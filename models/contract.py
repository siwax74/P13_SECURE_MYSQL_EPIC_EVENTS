from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey
from models.base import Base
from models.client import Client  # Assurez-vous que Client est importé
from models.user import User


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Relation avec Client pour stocker les informations du client
    client_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("clients.id"))
    client_information: Mapped[Optional["Client"]] = relationship("Client")

    # Relation avec User pour le commercial
    contact_commercial_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    contact_commercial: Mapped[Optional["User"]] = relationship("User")

    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    signed: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return (
            f"Contract(id={self.id}, client={self.client_information.name}, "
            f"commercial={self.contact_commercial.name}, total_amount={self.total_amount}, "
            f"remaining_amount={self.remaining_amount}, created_at={self.created_at}, "
            f"signed={self.signed})"
        )
