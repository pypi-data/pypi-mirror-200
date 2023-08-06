from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum
from lprp_core.data.model.model_base import ModelBase
from lprp_core.data.model.client import Client

if TYPE_CHECKING:
    from lprp_core.data.model.user import User
    from lprp_core.data.model.vehicle import Vehicle


class UsageLogState(Enum):
    PENDING = 0
    DONE = 1


class UsageLog(ModelBase):
    __tablename__ = "UsageLogs"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
    timestamp: Mapped[float] = mapped_column(default=None)
    user_username: Mapped[str] = mapped_column(
        ForeignKey("Users.username"), init=False, default=None, repr=False
    )
    user: Mapped[User] = relationship(init=False, default=None, back_populates="_usage_logs")
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("Vehicles.id"), init=False, default=None, repr=False, nullable=True
    )
    vehicle: Mapped[Vehicle] = relationship(init=False, default=None, back_populates="_usage_logs")

    client_id: Mapped[str] = mapped_column(
        ForeignKey("Clients.uuid"), init=False, default=None, repr=False
    )

    client: Mapped[Client] = relationship(init=False, default=None, back_populates="_usage_logs")

    image_path: Mapped[str] = mapped_column(default=None)

    log_state: Mapped[UsageLogState] = mapped_column(default=None)
