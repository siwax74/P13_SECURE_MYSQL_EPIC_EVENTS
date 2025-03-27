from datetime import datetime
from models.client import Client
from models.user import User


class Contract:
    def __init__(
        self,
        id: int,
        client: Client,
        commercial: User,
        total_amount: float,
        remaining_amount: float,
        created_at: datetime,
        signed: bool,
    ):
        self.id = id
        self.client = client
        self.commercial = commercial
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.created_at = created_at
        self.signed = signed

    def __str__(self):
        return (
            f"Contract(id={self.id}, client={self.client.name}, commercial={self.commercial.name}, "
            f"total_amount={self.total_amount}, remaining_amount={self.remaining_amount}, "
            f"created_at={self.created_at}, signed={self.signed})"
        )
