from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str 

class UserResponse(BaseModel):
    id: int
    username: str

class RegisterResponse(BaseModel):
    user: UserResponse
    message: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str