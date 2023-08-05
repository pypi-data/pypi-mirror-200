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


class Healthcheck(Service):
    PING_INTERVAL = 60  # seconds

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
    async def register_healthcheck(self, service: Service | str) -> Tuple[HealthcheckRegistration | None, Callable[[], bool] | None, bool]:
        """:param service: The service to register or name of the software/instance to register"""
        registration = HealthcheckRegistration(type=type(service).__name__ if isinstance(service, Service) else service)
        response: Response = requests.post(f"{self.address}/healthcheck/",
                                           json={"registration": registration.dict()})
        if response.status_code != 200:
            return None, None, False
        registration.id = response.json()['registration']["id"]

        def defined_availability_ping() -> bool:
            ping = AvailabilityPing(healthcheck_registration=registration,
                                    unix_time_of_sending=int(time.time()))
            r = requests.post(f"{self.address}/availability/ping", json={"availability_ping": ping.dict()})
            return r.status_code == 200

        defined_availability_ping()

        return registration, defined_availability_ping, response.status_code == 200

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
