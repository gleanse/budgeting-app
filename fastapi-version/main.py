from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select
from contextlib import asynccontextmanager
from typing import Annotated
from database import engine, get_session
from auth import create_access_token, get_current_user

# NOTE: import models to register them with SQLModels metadata
# without this import, create_all() wont know which tables to create so despite its show its not being use its still important to import models
from models import User
from auth_schemas import UserCreate, RegisterResponse, UserResponse


# STARTUP code that will first to run when server starts
# create all the database tables during start of the server, if the table already exist it will just ignore it
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SERVER - Server running...")
    print(f"Models registered: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(engine)
    print("DATABASE - All database tables created")
    yield
    print("SERVER - Shutting down...")

app = FastAPI(lifespan=lifespan)

DatabaseSession = Annotated[Session, Depends(get_session)]


@app.get("/")
async def root():
    print("Server Running")

    return {"message": "Budgeting App v0.1"}

@app.post("/register", response_model=RegisterResponse)
async def register_user(session: DatabaseSession, user_data: UserCreate):
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    new_user = User(username=user_data.username)
    new_user.set_password(user_data.password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return RegisterResponse(
        user=UserResponse(id=new_user.id, username=new_user.username),
        message="User created successfully",
    )

@app.post("/login")
async def login(session: DatabaseSession, form_data: OAuth2PasswordRequestForm = Depends()):

    # find user by username in database using orm sqlalchemy
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    # validate user exists and password is correct
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # generate token for the user
    access_token = create_access_token(username=user.username)

    return {"access_token": access_token, "token_type": "bearer"}
