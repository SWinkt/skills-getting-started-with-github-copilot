"""Tests for the POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]

    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "NonExistentActivity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_activities(client):
    # Arrange
    email = "versatile@mergington.edu"

    # Act - Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )

    # Act - Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify participant is in both activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]
