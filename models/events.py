from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey
from models.base import Base
from models.user import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    client_contact: Mapped[str] = mapped_column(String(255), nullable=False)
    event_start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    support_contact: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String)

    def __repr__(self):
        return f"<Event {self.name}>"
