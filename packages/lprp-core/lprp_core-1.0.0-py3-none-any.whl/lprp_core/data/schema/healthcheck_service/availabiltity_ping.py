from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from lprp_core.data.schema.healthcheck_service.healtcheck_registration import HealthcheckRegistration


class AvailabilityPing(BaseModel):
    healthcheck_registration: HealthcheckRegistration
    unix_time_of_sending: int