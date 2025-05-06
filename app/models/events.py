from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from app.models.base import Base
from app.models.contract import Contract
from app.models.user import User
from app.models.client import Client


class Event(Base):
    __tablename__ = "events"
    title: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    contract: Mapped[Optional["Contract"]] = relationship("Contract")
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    client: Mapped[Optional["Client"]] = relationship("Client")
    support_contact: Mapped[Optional["User"]] = relationship("User")
    start_datetime: Mapped[datetime] = mapped_column(DateTime)
    end_datetime: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str] = mapped_column(String)
    attendees: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
