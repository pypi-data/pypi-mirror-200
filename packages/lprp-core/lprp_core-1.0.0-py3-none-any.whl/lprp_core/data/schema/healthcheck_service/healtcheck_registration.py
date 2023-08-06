from pydantic import BaseModel


class HealthcheckRegistration(BaseModel):
    type: str | None  # name of service class
    id: str | None  # service id
