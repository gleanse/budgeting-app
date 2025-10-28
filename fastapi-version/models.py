from sqlmodel import Field, SQLModel
import bcrypt

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

    # hash password and store it
    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            salt
        ).decode("utf-8")

    # verify if password matches the hash
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), 
            self.password_hash.encode("utf-8")
        )