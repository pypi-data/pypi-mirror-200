"""
Guardian API websocket utilities.
"""
import os
import json
from dataclasses import dataclass, asdict
import socket
import datetime
import asyncio
from typing import Union
import requests
import websockets
import time
from dotenv import load_dotenv

from .config import settings
from .igeb_utils import unpack_from_queue
from .mock_utils import mock_cloud_package
from .debug_logs import (
    log_first_message,
    log_final_message,
    logging_connection,
    logging_break,
    logging_empty,
    logging_ping_error,
    logging_not_empty,
    log_interrupt_error,
    logging_connection_closed,
    logging_reconnection,
    logging_cloud_termination,
    logging_gaieerror,
    logging_cancelled_error,
    logging_connection_refused,
    logging_api_completed,
    logging_connecting_to_cloud,
    logging_cloud_not_receiving,
)

load_dotenv()


class GuardianAPI:
    """Main Guardian API client."""

    def __init__(self, debug: bool = True) -> None:
        """Initialize Guardian API client.

        Args:
            debug (bool, optional): Enable debug logging. Defaults to True.
        """
        self.debug: bool = debug
        self.ping_timeout: int = 2
        self.retry_time: int = 2
        self.base64string_len: int = 236
        self.first_message_check = True
        self.final_message_check = False
        self.payload_valid = True
        self.sample_rate = 250
        self.sentinal = object()
        self.encrypted_buffer_size = 3750  # 5 minutes => (5 * 60 * 250) / 20 = 3750
        self.decrypted_buffer_size = 75000  # 5 minutes => (5 * 60 * 250) = 75000
        self.encrypted_data_queue: asyncio.Queue = asyncio.Queue(
            maxsize=self.encrypted_buffer_size
        )
        self.decrypted_data_queue: asyncio.Queue = asyncio.Queue(
            maxsize=self.decrypted_buffer_size
        )
        self.initial_receipt_timeout = 15
        self.runtime_receipt_timeout = 1
        self.current_timeout = self.initial_receipt_timeout
        self.initial_bi_directional_timeout = 15
        self.runtime_bi_directional_timeout = 1
        self.bi_directional_timeout = self.initial_bi_directional_timeout
        self.last_saved_time = time.time()

    async def connect_ws_api(
        self,
        data_queue: asyncio.Queue,
        device_id: str = "deviceMockID",
        recording_id: str = "dummy_recID",
        impedance_measurement: bool = False,
    ) -> None:
        """Connect to the Guardian API websocket.

        Args:
            data_queue (asyncio.Queue): Data queue from the BLE client
            deviceID (str, optional): Device ID. Defaults to "deviceMockID".
            recordingID (str, optional): Recording ID. Defaults to "dummy_recID".

        Raises:
            Exception: If the websocket connection fails
        """

        def reset_data_model():
            data_model.payload = None
            data_model.impedance = None

        async def unpack_and_load_data():
            """Get data from the queue and pack it into a dataclass"""
            data_valid = False
            reset_data_model()
            package = await data_queue.get()
            (
                device_timestamp,
                device_id,
                data,
                stop,
                impedance,
            ) = unpack_from_queue(package)

            if data is not None:
                if len(data) == self.base64string_len:
                    data_model.payload = data
                    data_valid = True

            if impedance is not None:
                if isinstance(impedance, int):
                    data_model.impedance = impedance
                    data_valid = True

            if device_timestamp is not None:
                data_model.deviceTimestamp = device_timestamp

            if device_id is not None:
                data_model.deviceID = device_id

            if stop is not None:
                data_model.stop = stop
                if stop is True:
                    data_valid = True

            return data_valid

        async def create_timestamp(debug):
            """Create a timestamp for the data"""
            if data_queue.empty():
                logging_empty(debug)  # Fetch the current time from the device
                device_timestamp = datetime.datetime.now().astimezone().isoformat()
            else:
                logging_not_empty(debug)
                package = (
                    await data_queue.get()
                )  # Fetch the timestamp from the BLE package
                (device_timestamp, _, _, _, _) = unpack_from_queue(package)
            return device_timestamp

        async def unpack_and_load_data_termination():
            """Get data from the queue and pack it into a dataclass"""
            logging_cloud_termination(self.debug)
            data_model.payload = "STOP_CANCELLED"
            data_model.stop = True
            device_timestamp = await create_timestamp(self.debug)
            if device_timestamp is not None:
                data_model.deviceTimestamp = device_timestamp

        async def send_messages(websocket, data_model):
            while True:
                if await unpack_and_load_data():
                    await websocket.send(json.dumps(asdict(data_model)))
                    if not self.encrypted_data_queue.full():
                        await self.encrypted_data_queue.put(
                            [data_model.deviceTimestamp, data_model.payload]
                        )
                    else:
                        await self.encrypted_data_queue.get()

                if data_model.stop:
                    self.current_timeout = self.initial_receipt_timeout
                    break

        async def receive_messages(websocket):
            self.last_saved_time = time.time()
            while True:

                message_str = await asyncio.wait_for(
                    websocket.recv(), timeout=self.current_timeout
                )

                if "bp_filter_eeg" in message_str:
                    self.bi_directional_timeout = self.runtime_bi_directional_timeout
                    message = json.loads(message_str)
                    self.last_saved_time = time.time()
                    if not self.decrypted_data_queue.full():
                        self.decrypted_data_queue.put_nowait(message["bp_filter_eeg"])
                    else:
                        self.decrypted_data_queue.get_nowait()
                else:
                    self.current_timeout = self.runtime_receipt_timeout
                    if self.first_message_check:
                        self.first_message_check = False
                        log_first_message(
                            data_model,
                            message_str,
                            self.debug,
                        )
                    if data_model.stop:
                        log_final_message(
                            data_model,
                            message_str,
                            self.debug,
                        )
                        self.final_message_check = True
                        break

                time_without_data = time.time() - self.last_saved_time
                if (
                    time_without_data > self.bi_directional_timeout
                    and not impedance_measurement
                ):
                    raise asyncio.TimeoutError

        # initiate flags
        self.first_message_check = True
        self.final_message_check = False
        # Only when starting the code the first time do we want this to be the initial timeout

        # initiate data model
        data_model = GuardianDataModel(None, device_id, recording_id, None, None, False)

        while True:
            logging_connecting_to_cloud(self.debug)
            try:
                async with websockets.connect(settings.WS_IDENTIFIER) as websocket:  # type: ignore
                    try:
                        self.first_message_check = True
                        # for the websocket we want to increase to initial timeout each time
                        self.bi_directional_timeout = (
                            self.initial_bi_directional_timeout
                        )
                        self.current_timeout = self.initial_receipt_timeout

                        logging_connection(settings.WS_IDENTIFIER, self.debug)
                        send_task = asyncio.create_task(
                            send_messages(websocket, data_model)
                        )
                        receive_task = asyncio.create_task(receive_messages(websocket))
                        await asyncio.gather(send_task, receive_task)

                    except (
                        asyncio.TimeoutError,
                        websockets.exceptions.ConnectionClosed,  # type: ignore
                    ) as error:
                        log_interrupt_error(error, self.debug)
                        try:
                            # Wait for the ping timeout before trying to reconnect
                            # If it is the bi-directional timeout, then we want to
                            # wait a bit even though we can still send data
                            await asyncio.sleep(self.ping_timeout)
                            logging_connection_closed(self.debug)
                            pong = await websocket.ping()
                            # If the bi-directional timeout is reached, then we
                            # we will get a pong immediately, if it is the
                            await asyncio.wait_for(pong, timeout=self.ping_timeout)
                            logging_reconnection(self.debug)
                            self.bi_directional_timeout = (
                                self.initial_bi_directional_timeout
                            )
                            continue
                        except Exception as error:
                            logging_ping_error(error, self.ping_timeout, self.debug)
                            await asyncio.sleep(self.ping_timeout)

                    except asyncio.CancelledError as error:
                        async with websockets.connect(  # type: ignore
                            settings.WS_IDENTIFIER
                        ) as websocket:
                            logging_cancelled_error(error, self.debug)
                            await unpack_and_load_data_termination()

                            await websocket.send(json.dumps(asdict(data_model)))
                            package_receipt = await websocket.recv()

                            log_final_message(
                                data_model,
                                package_receipt,
                                self.debug,
                            )
                            self.final_message_check = True
                            break

            except socket.gaierror as error:
                logging_gaieerror(error, self.retry_time, self.debug)
                await asyncio.sleep(self.retry_time)
                continue

            except ConnectionRefusedError as error:
                logging_connection_refused(error, self.retry_time, self.debug)
                await asyncio.sleep(self.retry_time)
                continue

            if self.final_message_check:
                logging_break(self.debug)
                break

        logging_api_completed(self.debug)

    def get_recordings_info_all(
        self, device_id: str = "mock-device-0", first_to_last=False, password: str = ""
    ) -> list:
        recordings_url = f"{settings.REST_API_LOGIN}recordings"
        if password == "":
            password = input("\nEnter your new passsword here: ")
        with requests.Session() as session:
            result = session.get(recordings_url, auth=(device_id, password))
            if result.status_code == 200:
                print("Recording list retrieved successfully")
                recordings = result.json()
                recordings.sort(
                    key=lambda x: datetime.datetime.strptime(
                        x["startDeviceTimestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    reverse=first_to_last,
                )
                print(json.dumps(recordings, indent=4, sort_keys=True))
                return result.json()
            elif result.status_code == 401:
                print(f"Password for {device_id} is incorrect")
                return []
            elif result.status_code == 403:
                print(
                    "Wrong device ID, you can find the device ID in",
                    " the logs in the format XX-XX-XX-XX-XX-XX",
                )
                return []
            elif result.status_code == 412:
                print(
                    f"Device {device_id} is not registered",
                )
                return []
            elif result.status_code == 404:
                print(f"No recording found for device {device_id}")
                return []
            elif result.status_code == 502:
                print(f"Device {device_id} does not exist")
                return []
            else:
                print("Loading recording list failed")
                return []

    def get_recording_info_by_id(
        self, device_id: str, recording_id: str = "recordingId-0", password: str = ""
    ) -> list:
        recordings_url = f"{settings.REST_API_LOGIN}recordings/{recording_id}"

        if password == "":
            password = input("\nEnter your new passsword here: ")
        with requests.Session() as session:
            result = session.get(recordings_url, auth=(device_id, password))
            if result.status_code == 200:
                print("Recording ID file found")
                print(json.dumps(result.json(), indent=4, sort_keys=True))
                return result.json()
            elif result.status_code == 401:
                print(f"Password for {device_id} is incorrect")
                return []
            elif result.status_code == 403:
                print(
                    "Wrong device ID, you can find the device ID in",
                    " the logs in the format XX-XX-XX-XX-XX-XX",
                )
                return []
            elif result.status_code == 412:
                print(
                    f"Device {device_id} not registered",
                )
                return []
            elif result.status_code == 404:
                print(f"No recording found for {device_id} and {recording_id}")
                return []
            elif result.status_code == 502:
                print(f"Device {device_id} does not exits")
                return []
            else:
                print("Recording not found")
                print(result.status_code)
                print(result.json())
                return []

    def download_recording_by_id(
        self, device_id: str, recording_id: str = "recordingId-0", password: str = ""
    ) -> None:
        """Download the recording by ID and save it to the recordings folder"""

        recordings_folder_name = "recordings"
        recording_subfolder_name = recording_id

        if password == "":
            password = input("\nEnter your new passsword here: ")
        recording_types = ["eeg", "imu"]
        for data_type in recording_types:
            with requests.Session() as session:

                record_url_first = f"{settings.REST_API_LOGIN}recordings/"
                record_url_second = f"{recording_id}/download/{data_type}"
                record_url = record_url_first + record_url_second
                result = session.get(record_url, auth=(device_id, password))

                if result.status_code == 200:

                    print(f"Recording ID file found, downloading {data_type} data")
                    print(result.json())

                    # Creating folder for recording
                    folder_path = os.path.join(
                        recordings_folder_name, recording_subfolder_name
                    )
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    # get url from responsex
                    url = result.json()["downloadUrl"]
                    result = session.get(url)
                    filename = f"{recording_id}_{data_type}.csv"
                    file_path = os.path.join(folder_path, filename)

                    print(f"Writing to file: {file_path}")
                    with open(file_path, "wb") as file:
                        file.write(result.content)

                    print("Downloading complete for recording ID: ", recording_id)

                elif result.status_code == 401:
                    if data_type == "eeg":
                        print(f"Password for {device_id} is incorrect")

                elif result.status_code == 403:
                    if data_type == "eeg":
                        print(
                            "Wrong device ID, you can find the device ID in",
                            " the logs in the format XX-XX-XX-XX-XX-XX",
                        )
                elif result.status_code == 412:
                    if data_type == "eeg":
                        print(f"Device {device_id} is not registered")
                elif result.status_code == 404:
                    print(f"No {data_type} recording found for this device ID")
                elif result.status_code == 502:
                    if data_type == "eeg":
                        print(f"Device {device_id} does not exist")
                else:
                    if data_type == "eeg":
                        print("Data download failed")
                        print(result.status_code)
                        print(result.json())


@dataclass
class GuardianDataModel:
    """Data model for Guardian data"""

    deviceTimestamp: Union[str, None]
    deviceID: Union[str, None]
    recordingID: Union[str, None]
    payload: Union[str, None]  # This is a base64 encoded bytearray as a string
    impedance: Union[int, None]
    stop: Union[bool, None]
