from sqlmodel import Session, select
from app.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def save(self, user: User) -> User:
        """insert or update user"""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
