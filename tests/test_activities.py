"""Tests for the GET /activities endpoint using AAA pattern"""


def test_get_activities_success(client):
    # Arrange - No setup needed, activities data is pre-loaded in app

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert all("description" in activity for activity in activities.values())
    assert all("schedule" in activity for activity in activities.values())
    assert all("max_participants" in activity for activity in activities.values())
    assert all("participants" in activity for activity in activities.values())


def test_get_activities_has_participants(client):
    # Arrange - No setup needed

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    assert isinstance(activities["Chess Club"]["participants"], list)
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]


def test_get_activities_returns_correct_structure(client):
    # Arrange - No setup needed

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
