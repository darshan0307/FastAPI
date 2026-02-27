import pytest
from app import models, schemas


@pytest.fixture()
def test_vote(test_user, session):
    """Fixture to create a test vote. """
    new_vote = models.Vote(post_id=1, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    """Test voting on a post. """
    post_id = test_posts[0].id
    response = authorized_client.post("/votes/", json={
        "post_id": post_id,
        "dir": 1
    })
    assert response.status_code == 201
    assert response.json() == {"message": "Successfully added vote."}


def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    """Test voting on a post twice. """
    post_id = test_posts[0].id
    response = authorized_client.post("/votes/", json={
        "post_id": post_id,
        "dir": 1
    })
    assert response.status_code == 409
    assert response.json() == {"detail": "You have already voted on this post."}


def test_delete_vote(authorized_client, test_posts, test_vote):
    """Test deleting a vote. """
    post_id = test_posts[0].id
    response = authorized_client.post("/votes/", json={
        "post_id": post_id,
        "dir": 0
    })
    assert response.status_code == 201
    assert response.json() == {"message": "Successfully deleted vote."}

def test_delete_nonexistent_vote(authorized_client, test_posts):
    """Test deleting a vote that does not exist. """
    post_id = test_posts[0].id
    response = authorized_client.post("/votes/", json={
        "post_id": post_id,
        "dir": 0
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Vote does not exist."}


def test_vote_on_nonexistent_post(authorized_client):
    """Test voting on a post that does not exist. """
    response = authorized_client.post("/votes/", json={
        "post_id": 9999,
        "dir": 1
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Post does not exist."}