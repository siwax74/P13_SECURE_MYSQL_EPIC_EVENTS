from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, Boolean, DateTime, ForeignKey
from app.models.base import Base
from app.models.client import Client
from app.models.user import User


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("clients.id"))
    client: Mapped[Optional["Client"]] = relationship("Client")
    contact_commercial_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    contact_commercial: Mapped[Optional["User"]] = relationship("User")
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
