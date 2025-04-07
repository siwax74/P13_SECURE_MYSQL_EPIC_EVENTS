from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey
from models.base import Base
from models.user import User


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_information: Mapped[str] = mapped_column(String, nullable=False)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    commercial: Mapped["User"] = relationship(back_populates="contracts")
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    signed: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return (
            f"Contract(id={self.id}, client={self.client}, commercial={self.commercial.name}, "
            f"total_amount={self.total_amount}, remaining_amount={self.remaining_amount}, "
            f"created_at={self.created_at}, signed={self.signed})"
        )
