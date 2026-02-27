from app import schemas

def test_root(client):
    """Test the root endpoint. """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_create_user(client):
    """Test creating a new user. """
    response = client.post(
        "/user/", json={"email": "bhumi@1123.com", "password": "password123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "bhumi@1123.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    """Test logging in a user. """
    response = client.post(
        "/login/", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200
    assert "access_token" in response.json()


    