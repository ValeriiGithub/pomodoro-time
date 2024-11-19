from dataclasses import dataclass

from schema import UserLoginSchema
from repository import UserRepository
from service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    user_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username=username, password=password)
        access_token = self.user_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
