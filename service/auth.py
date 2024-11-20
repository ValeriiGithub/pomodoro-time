from dataclasses import dataclass
import datetime as dt
from datetime import timedelta

from jose import jwt

from models import UserProfile
from exception import UserNotFoundException, UserNotCorrectPasswordException
from repository import UserRepository
from schema import UserLoginSchema
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException


    def generate_access_token(self, user_id: int) -> str:
        # Возможный fix baga
        # expire_date = dt.datetime.now(dt.timezone.utc) + timedelta(days=7)  # Expire in 7 days
        # expire_date_unix = expire_date.timestamp()
        expire_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()  # Expire in 1 day
        token = jwt.encode(
            {'user_id': user_id, 'expire': expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM,
        )
        return token
