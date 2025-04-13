from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from models.base import Base
from models.user import User
from models.client import Client


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    contract_id: Mapped[int] = mapped_column(Integer)

    # Foreign keys
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationships
    client: Mapped[Optional["Client"]] = relationship("Client")
    support_contact: Mapped[Optional["User"]] = relationship("User")

    start_datetime: Mapped[datetime] = mapped_column(DateTime)
    end_datetime: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str] = mapped_column(String)
    attendees: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
