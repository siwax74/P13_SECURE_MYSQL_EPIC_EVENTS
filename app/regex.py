import re


@staticmethod
def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


@staticmethod
def is_valid_phone(phone):
    pattern = r"^\+?(\d{1,3})?[\s\-]?\(?(\d{2})\)?[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}$"
    return re.match(pattern, phone) is not None


@staticmethod
def is_valid_name(name):
    pattern = r"^[a-zA-ZÀ-ÿ\s\'-]+$"
    return re.match(pattern, name) is not None


@staticmethod
def is_valid_company(company):
    pattern = r"^[a-zA-Z0-9À-ÿ\s\.\-]+$"
    return re.match(pattern, company) is not None


@staticmethod
def is_valid_id(id_value):
    return bool(re.match(r"^\d+$", str(id_value)))


@staticmethod
def is_valid_amount(self, value):
    try:
        return bool(re.match(r"^\d+(\.\d{1,2})?$", str(value)))
    except ValueError:
        return False

@staticmethod
def is_valid_title(title):
    return bool(re.match(r"^.{1,255}$", title))

@staticmethod
def is_valid_datetime(value):
    return bool(re.match(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$", value))

@staticmethod
def is_valid_location(location):
    return bool(re.match(r"^.{1,255}$", location))

@staticmethod
def is_valid_attendees(attendees):
    return bool(re.match(r"^\d+$", str(attendees)))

@staticmethod
def is_valid_notes(notes):
    return bool(re.match(r"^.{0,1000}$", notes))

@staticmethod
def is_valid_username(username: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_.-]{3,20}$", username))

@staticmethod
def is_valid_password(password: str) -> bool:
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$", password))
