from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from alembic import command
from app import models
from app.oauth2 import create_access_token

# ensure the test database exists before SQLAlchemy tries to connect
TEST_DB_NAME = f"{settings.database_name}_test"
def _create_test_db():
    conn = psycopg2.connect(host=settings.database_hostname,
                            user=settings.database_username,
                            password=settings.database_password,
                            port=settings.database_port,
                            dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TEST_DB_NAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE \"{TEST_DB_NAME}\"")
    cur.close()
    conn.close()

_create_test_db()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{TEST_DB_NAME}"

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


@pytest.fixture(scope="function")
def session():
    """Fixture for the database session.

    Runs for each test to ensure a clean database state.  Dropping and
    recreating all tables on every function is slower but keeps tests
    isolated and avoids unique-key conflicts.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
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
    """Fixture for creating a test user with a unique email per invocation."""
    import uuid
    email = f"test_{uuid.uuid4().hex}@example.com"
    user_data = {"email": email, "password": "password123"}
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


@pytest.fixture
def test_posts(test_user, session):
    """Fixture for creating test posts. """
    posts_data = [
        {"title": "First Post", "content": "Content of the first post", "owner_id": test_user['id']},
        {"title": "Second Post", "content": "Content of the second post", "owner_id": test_user['id']},
        {"title": "Third Post", "content": "Content of the third post", "owner_id": test_user['id']}
    ]
    posts = []
    for post_data in posts_data:
        post = models.Post(**post_data)
        session.add(post)
        session.commit()
        session.refresh(post)
        posts.append(post)
    return posts


