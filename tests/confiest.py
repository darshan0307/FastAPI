from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from alembic import command


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
                        autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)   

# def override_get_db():
#     db = TestingSessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()


app.dependency_overrides[get_db] = get_db


@pytest.fixture(scope="module")
def session():
    """Fixture for the database session. """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    """Fixture for the test client. """
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = lambda: session
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    """Fixture for creating a test user. """
    user_data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/user/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    """Fixture for creating an access token for the test user. """
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    """Fixture for creating an authorized test client. """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client




