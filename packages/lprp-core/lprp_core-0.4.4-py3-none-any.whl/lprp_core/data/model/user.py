from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from lprp_core.data.model.model_base import ModelBase
from lprp_core.data.model.vehicle import Vehicle
from lprp_core.data.model.usage_log import UsageLog

if TYPE_CHECKING:
    pass


class User(ModelBase):
    __tablename__ = "Users"

    username: Mapped[str] = mapped_column(default=None, primary_key=True)
    first_name: Mapped[str] = mapped_column(default=None)
    last_name: Mapped[str] = mapped_column(default=None)
    email: Mapped[str] = mapped_column(default=None, unique=True)
    passwd: Mapped[str] = mapped_column(default=None)
    admin: Mapped[bool] = mapped_column(default=False)
    vehicles: List[Vehicle] = field(init=False, default_factory=list)
    _vehicles: Mapped[List[Vehicle]] = relationship(
        init=False, default_factory=list, repr=False, back_populates="user"
    )
    usage_logs: List[UsageLog] = field(init=False, default_factory=list)
    _usage_logs: Mapped[List[UsageLog]] = relationship(
        init=False, default_factory=list, repr=False, back_populates="user"
    )

    @property
    def vehicles(self) -> list[vehicles]:
        return self._vehicles

    @vehicles.setter
    def vehicles(self, vehicles: list[Vehicle]):
        if isinstance(vehicles, list):
            for vehicle in vehicles:
                vehicle.user = self
            self._vehicles = vehicles
        else:
            self._vehicles = []

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
