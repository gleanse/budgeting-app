from sqlmodel import Field, SQLModel
from passlib.context import CryptContext

# 'schemes' defining hasing algo that will use and then 'deprecated=auto ' update old password hashes
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

    # hash password and store it
    def set_password(self, password: str):
        self.password_hash = password_hasher.hash(password)

    # verify if password matches the hash
    def verify_password(self, password: str) -> bool:
        return password_hasher.verify(password, self.password_hash)