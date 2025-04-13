from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from models.base import Base
from models.user import User


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relation avec User
    contact_commercial_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    contact_commercial: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self):
        return (
            f"Client(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', "
            f"company='{self.company}', created_at='{self.created_at}', updated_at='{self.updated_at}', "
            f"contact_commercial='{self.contact_commercial.username if self.contact_commercial else None}')"
        )
