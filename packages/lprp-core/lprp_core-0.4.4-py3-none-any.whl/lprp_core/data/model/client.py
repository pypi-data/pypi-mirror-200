from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from lprp_core.data.model.model_base import ModelBase
from lprp_core.data.model.parking_garage import ParkingGarage

if TYPE_CHECKING:
    from lprp_core.data.model.usage_log import UsageLog


class Client(ModelBase):
    __tablename__ = "Clients"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
    parking_garage_id: Mapped[int] = mapped_column(
        ForeignKey("ParkingGarages.id"), init=False, default=None, repr=False, nullable=True
    )
    parking_garage: Mapped[ParkingGarage] = relationship(init=False, default=None, back_populates="_clients")
    go_out: Mapped[bool] = mapped_column(default=False)
    usage_logs: List[UsageLog] = field(init=False, default_factory=list)
    _usage_logs: Mapped[List[UsageLog]] = relationship(
        init=False, default_factory=list, repr=False  # , back_populates="client"
    )

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
