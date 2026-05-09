import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from decouple import config
from app.main import app
from app.database import get_session

TEST_DATABASE_URL = config("TEST_DATABASE_URL")
TEST_USERNAME = "testuser"
TEST_PASSWORD = "password123"
TEST_CATEGORY = {"name": "Salary", "type": "income"}
TEST_CATEGORY_EXPENSE = {"name": "Food", "type": "expense"}

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


@pytest.fixture()
def token(client):
    client.post(
        "/api/v1/auth/register",
        json={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    return response.json()["access_token"]


@pytest.fixture()
def headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def created_category(client, headers):
    response = client.post("/api/v1/categories/", json=TEST_CATEGORY, headers=headers)
    return response.json()["created_item"]
