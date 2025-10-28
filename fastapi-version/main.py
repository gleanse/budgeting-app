from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel
from contextlib import asynccontextmanager
from typing import Annotated
from database import engine, get_session

# NOTE: import models to register them with SQLModels metadata
# without this import, create_all() wont know which tables to create so despite its show its not being use its still important to import models
from models import User


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