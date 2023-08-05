from __future__ import annotations

from dataclasses import field
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lprp_core.data.model.model_base import ModelBase
from lprp_core.data.model.usage_log import UsageLog

if TYPE_CHECKING:
    from lprp_core.data.model.user import User


class VehicleType(Enum):
    CAR = "car"
    TRUCK = "truck"
    BUS = "bus"
    MOTORBIKE = "motorbike"
    OTHER = "other"


class Vehicle(ModelBase):
    __tablename__ = "Vehicles"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    vehicle_type: VehicleType = field(init=False, default=None)
    _vehicle_type: Mapped[str] = mapped_column(init=False, default=None)
    license_plate: Mapped[str] = mapped_column(init=False, default=None, unique=True)
    user_username: Mapped[str] = mapped_column(
        ForeignKey("Users.username"), init=False, default=None, repr=False
    )
    user: Mapped[User] = relationship(init=False, default=None)
    usage_logs: List[UsageLog] = field(init=False, default_factory=list)
    _usage_logs: Mapped[List[UsageLog]] = relationship(
        init=False, default_factory=list, repr=False  # , back_populates="vehicle"
    )

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value):
        self._vehicle_type = value

    @property
    def usage_logs(self) -> list[usage_logs]:
        return self._usage_logs

    @usage_logs.setter
    def usage_logs(self, usage_logs: list[UsageLog]):
        if isinstance(usage_logs, list):
            for usage_log in usage_logs:
                usage_log.user = self
            self._usage_logs = usage_logs
        else:
            self._usage_logs = []
