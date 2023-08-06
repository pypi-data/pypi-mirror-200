import asyncio
import threading
import time
import uuid
from enum import Enum
from typing import Callable, Tuple

import requests
from requests import Response

from lprp_core.data.schema.healthcheck_service.availabiltity_ping import AvailabilityPing
from lprp_core.data.schema.healthcheck_service.healtcheck_registration import HealthcheckRegistration
from lprp_core.service import Service, optionally_syncronized


class HealthStatus(Enum):
    HEALTHY = 0
    INCREASED_RISK = 1
    TEMPORARY_ISSUE = 2
    MAJOR_ISSUE = 3
    UNDEFINED = 4


class HealthcheckPinger:
    def __init__(self, start_function: Callable[[], None], stop_function: Callable[[], None]):
        self.start_function = start_function
        self.stop_function = stop_function

    def __enter__(self):
        self.start_function()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop_function()


class Healthcheck(Service):
    PING_INTERVAL = 5  # seconds

    def __init__(self, address: str):
        self.address = address

    @optionally_syncronized
    async def is_available(self) -> bool:
        response = requests.get(f"{self.address}/is_available")
        if response.status_code != 200:
            return False
        return response.json()["is_available"]

    @optionally_syncronized
    async def get_current_health(self) -> HealthStatus | None:
        response = requests.get(f"{self.address}/health/current")
        if response.status_code != 200:
            return None
        return HealthStatus(response.json()["health"])

    @optionally_syncronized
    async def register_healthcheck(self, service: Service | str) -> Tuple[
        HealthcheckRegistration | None, HealthcheckPinger | None, bool]:
        """
        :param service: The service to register or name of the software/instance to register
        :return: registration, Pinger(ContextManager), success

        usage:
        ```python
        registration, pinger, success = service.register_healthcheck(service_to_test, sync=True)
        with pinger:
            do_stuff()
        ```
        """
        registration = HealthcheckRegistration(type=type(service).__name__ if isinstance(service, Service) else service)
        response: Response = requests.post(f"{self.address}/healthcheck/",
                                           json={"registration": registration.dict()})
        if response.status_code != 200:
            return None, None, False
        registration.id = response.json()['registration']["id"]

        break_event: threading.Event = threading.Event()

        def defined_availability_ping():
            while not break_event.is_set():
                ping = AvailabilityPing(healthcheck_registration=registration,
                                        unix_time_of_sending=int(time.time()))
                r = requests.post(f"{self.address}/availability/ping", json={"availability_ping": ping.dict()})
                time.sleep(Healthcheck.PING_INTERVAL - 1)
            return

        thread = None

        def start() -> None:
            nonlocal thread
            thread = threading.Thread(target=defined_availability_ping)
            thread.start()

        def stop() -> None:
            nonlocal thread
            break_event.set()
            thread.join()

        return registration, HealthcheckPinger(start, stop), response.status_code == 200

    @optionally_syncronized
    async def delete_healthcheck(self, registration: HealthcheckRegistration) -> bool:
        response: Response = requests.delete(f"{self.address}/healthcheck/",
                                             json={"registration": registration.dict()})
        return response.status_code == 200

    @optionally_syncronized
    async def availability_ping(self, availability_ping: AvailabilityPing) -> bool:
        response: Response = requests.get(f"{self.address}/availability/ping",
                                          json={"availability_ping": availability_ping.dict()})
        return response.status_code == 200
