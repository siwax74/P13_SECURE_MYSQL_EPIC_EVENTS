from models.user import User


class Client:
    def __init__(self, id, name, email, phone, company, created_at, updated_at, contact_commercial: User):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.created_at = created_at
        self.updated_at = updated_at
        self.contact_commercial = contact_commercial if contact_commercial.is_commercial else None

    def __str__(self):
        return (
            f"Client(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', "
            f"company='{self.company}', created_at='{self.created_at}', updated_at='{self.updated_at}', "
            f"contact_commercial='{self.contact_commercial}')"
        )
