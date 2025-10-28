from sqlmodel import SQLModel

class UserCreate(SQLModel):
    username: str
    password: str 

class UserResponse(SQLModel):
    id: int
    username: str

class RegisterResponse(SQLModel):
    user: UserResponse
    message: str

class LoginResponse(SQLModel):
    access_token: str
    token_type: str