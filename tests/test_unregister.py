"""Tests for the DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""


def test_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_activity_not_found(client):
    # Arrange
    activity_name = "NonExistentActivity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_then_signup_again(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "ava@mergington.edu"  # Already registered

    # Act - Unregister
    response1 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Act - Sign up again
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify participant is registered again
    activities_response = client.get("/activities")
    assert email in activities_response.json()["Tennis Club"]["participants"]
