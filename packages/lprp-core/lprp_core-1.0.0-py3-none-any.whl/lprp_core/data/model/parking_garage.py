from __future__ import annotations

from typing import TYPE_CHECKING, List

from dataclasses import field
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lprp_core.data.model.model_base import ModelBase

if TYPE_CHECKING:
    from lprp_core.data.model.client import Client


class ParkingGarage(ModelBase):
    __tablename__ = 'ParkingGarages'

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    name: Mapped[str] = mapped_column(default=None)
    car_space: Mapped[int] = mapped_column(default=0)
    car_current: Mapped[int] = mapped_column(default=0)
    motorbike_space: Mapped[int] = mapped_column(default=0)
    motorbike_current: Mapped[int] = mapped_column(default=0)
    bus_space: Mapped[int] = mapped_column(default=0)
    bus_current: Mapped[int] = mapped_column(default=0)
    truck_space: Mapped[int] = mapped_column(default=0)
    truck_current: Mapped[int] = mapped_column(default=0)
    other_space: Mapped[int] = mapped_column(default=0)
    other_current: Mapped[int] = mapped_column(default=0)
    clients: List[Client] = field(init=False, default_factory=list)
    _clients: Mapped[List[Client]] = relationship(
        init=False, default_factory=list, repr=False, back_populates="parking_garage"
    )

    @property
    def clients(self) -> list[clients]:
        return self._clients

    @clients.setter
    def clients(self, clients: list[clients]):
        if isinstance(clients, list):
            for client in clients:
                client.user = self
            self._clients = clients
        else:
            self._clients = []
