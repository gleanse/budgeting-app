from sqlmodel import Session
from app.models import User
from app.schemas.auth_schema import UserCreate
from app.repositories.user_repository import UserRepository
from app.core.auth_core import create_access_token

class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)

    def register_user(self, user_data: UserCreate):
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")
        
        new_user = User(username=user_data.username)
        new_user.set_password(user_data.password)
        
        return self.user_repo.add_new_user(new_user)

    def login(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)

        if not user or not user.verify_password(password):
            raise ValueError("Invalid username or password")
        
        access_token = create_access_token(username=user.username)
        
        return access_token