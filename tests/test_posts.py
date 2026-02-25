import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_user):
    """Test retrieving all posts. """
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    for post in posts:
        assert "id" in post
        assert "title" in post
        assert "content" in post
        assert "owner_id" in post


def test_unauthorized_user_get_all_posts(client):
    """Test that unauthorized users cannot retrieve posts. """
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_single_post(client, test_posts):
    """Test that unauthorized users cannot retrieve a single post. """
    post_id = test_posts[0].id
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 401

def test_get_single_post_not_exist(authorized_client):
    """Test retrieving a single post that does not exist. """
    response = authorized_client.get("/posts/9999")
    assert response.status_code == 404

def test_get_single_post(authorized_client, test_posts):
    """Test retrieving a single post. """
    post_id = test_posts[0].id
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == post_id
    assert "title" in post
    assert "content" in post
    assert "owner_id" in post


@pytest.mark.parametrize("title, content, published", [
    ("New Post", "Content of the new post", True),
    ("Another Post", "Content of another post", False)
]) 
def test_create_post(authorized_client, title, content, published):
    """Test creating a new post. """
    response = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    assert response.status_code == 201
    post = response.json()
    assert post["title"] == title
    assert post["content"] == content
    assert post["published"] == published


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    """Test creating a post with default published value. """
    response = authorized_client.post("/posts/", json={
        "title": "Default Published Post",
        "content": "Content of the post with default published value"
    })
    assert response.status_code == 201
    post = response.json()
    assert post["published"] == True


def test_unauthorized_user_create_post(client):
    """Test that unauthorized users cannot create posts. """
    response = client.post("/posts/", json={
        "title": "Unauthorized Post",
        "content": "Content of the unauthorized post"
    })
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    """Test that unauthorized users cannot delete posts. """
    post_id = test_posts[0].id
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 401


def test_delete_post_not_exist(authorized_client):
    """Test deleting a post that does not exist. """
    response = authorized_client.delete("/posts/9999")
    assert response.status_code == 404


def test_delete_post(authorized_client, test_posts):
    """Test deleting a post. """
    post_id = test_posts[0].id
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    # Verify the post is deleted
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 404  



def test_update_post(authorized_client, test_posts):
    """Test updating a post. """
    post_id = test_posts[0].id
    response = authorized_client.put(f"/posts/{post_id}", json={
        "title": "Updated Title",
        "content": "Updated content",
        "published": False
    })
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == "Updated Title"
    assert post["content"] == "Updated content"
    assert post["published"] == False


def test_update_post_not_exist(authorized_client):
    """Test updating a post that does not exist. """
    response = authorized_client.put("/posts/9999", json={
        "title": "Non-existent Post",
        "content": "Content of the non-existent post",
        "published": True
    })
    assert response.status_code == 404