from sqlmodel import create_engine, Session
from decouple import config

engine = create_engine(config('DATABASE_URL'))

# automatically open the database connection session and then automatically close it after using it
# 'with' automatically open and close the database session when function ends
# 'yield' pause the function to pass session to fastapi after using the session the it will now continue the function
def get_session():
    with Session(engine) as session:
        yield session