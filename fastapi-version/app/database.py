from sqlmodel import create_engine, Session
from decouple import config

engine = create_engine(config("DATABASE_URL"))


# automatically open the database connection session and then automatically close it after using it
def get_session():
    with Session(engine) as session:
        yield session
