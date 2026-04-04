from sqlmodel import Session
from app.models import User
from app.repositories.user_repository import UserRepository
from app.core.auth_core import create_access_token


class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)

    def register_user(self, username: str, password: str) -> User:
        if self.user_repo.get_by_username(username):
            raise ValueError("Username already exists")

        new_user = User(username=username)
        new_user.set_password(password)

        return self.user_repo.add(new_user)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(username)

        if not user or not user.verify_password(password):
            raise ValueError("Invalid username or password")

        access_token = create_access_token(username=user.username)

        return access_token
