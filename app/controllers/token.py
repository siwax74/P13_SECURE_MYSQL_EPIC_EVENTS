import json
import jwt
import os
from datetime import datetime, timedelta
from app.models.user import User
from sqlalchemy.orm import Session

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
TOKEN_FILE_PATH = "token.jwt"


class ObtainToken:
    def __init__(self, session: Session, user: User):
        self.session = session
        self.user = user

    def create_tokens(self) -> dict:
        access_expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        access_payload = {"user_id": self.user.id, "email": self.user.email, "exp": access_expire, "type": "access"}

        refresh_payload = {"user_id": self.user.id, "email": self.user.email, "exp": refresh_expire, "type": "refresh"}

        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

        self._store_tokens(access_token, refresh_token, access_expire)

        return {"access_token": access_token, "refresh_token": refresh_token, "expires_at": access_expire.isoformat()}

    def _store_tokens(self, access_token: str, refresh_token: str, expires_at: datetime):
        data = {
            "user": self.user.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.isoformat(),
        }
        with open(TOKEN_FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)

    def get_stored_tokens(self) -> dict | None:
        if os.path.exists(TOKEN_FILE_PATH):
            with open(TOKEN_FILE_PATH, "r") as f:
                return json.load(f)
        return None


class RefreshToken:
    def __init__(self, session: Session, user: User, token: str):
        self.session = session
        self.user = user
        self.token = token

    def update_token(self):
        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != "refresh":
                raise jwt.InvalidTokenError("Invalid token type")

            new_access_expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            new_access_payload = {
                "user_id": self.user.id,
                "email": self.user.email,
                "exp": new_access_expire,
                "type": "access",
            }

            new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm=ALGORITHM)

            new_refresh_expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            new_refresh_payload = {
                "user_id": self.user.id,
                "email": self.user.email,
                "exp": new_refresh_expire,
                "type": "refresh",
            }

            new_refresh_token = jwt.encode(new_refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

            self._store_new_tokens(new_access_token, new_refresh_token, new_access_expire)

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "expires_at": new_access_expire.isoformat(),
            }

        except jwt.ExpiredSignatureError:
            raise Exception("Refresh token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid refresh token")

    def _store_new_tokens(self, access_token: str, refresh_token: str, expires_at: datetime):
        data = {
            "user": self.user.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.isoformat(),
        }
        with open(TOKEN_FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)
