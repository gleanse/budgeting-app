from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class UserCreateResponse(BaseModel):
    message: str = "User created successfully"
    user: UserResponse


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
