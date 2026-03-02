"""Tests for the root endpoint using AAA pattern"""


def test_root_redirect(client):
    # Arrange - No setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_follows(client):
    # Arrange - No setup needed

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert - FastAPI serves redirects (may not have full HTML, but status should be 200)
    assert response.status_code == 200
