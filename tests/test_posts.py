def test_get_all_posts(authorized_client):
    """Test getting all posts. """
    response = authorized_client.get("/posts/")
    assert response.status_code == 200