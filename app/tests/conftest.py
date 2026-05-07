import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from decouple import config
from app.main import app
from app.database import get_session

TEST_DATABASE_URL = config("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)

# for isolated individual methods and services that interact with the database directly
@pytest.fixture()
def session():
    with test_engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection) as session:
            yield session
        # undo/cleanup all DB writes after each test
        transaction.rollback()

# for testing api endpoints
@pytest.fixture()
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()