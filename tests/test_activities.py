"""
Tests for GET /activities endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Use fixtures to set up the test client and reset app state
- Act: Make GET request to /activities endpoint
- Assert: Verify response structure, status code, and content
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """
        AAA Test: GET /activities returns successful response.
        
        Arrange: Use fresh client from fixture with initial activities state
        Act: Make GET request to /activities
        Assert: Verify status code is 200
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """
        AAA Test: GET /activities returns all 9 activities.
        
        Arrange: Use fresh client from fixture with all 9 activities
        Act: Make GET request to /activities
        Assert: Verify all activities are returned in response
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
        ]
        assert set(data.keys()) == set(expected_activities)
        assert len(data) == 9

    @pytest.mark.parametrize("activity_name,expected_description,expected_max", [
        ("Chess Club", "Learn strategies and compete in chess tournaments", 12),
        ("Programming Class", "Learn programming fundamentals and build software projects", 20),
        ("Gym Class", "Physical education and sports activities", 30),
        ("Basketball Team", "Competitive basketball team and practice sessions", 15),
        ("Tennis Club", "Learn tennis skills and compete in matches", 20),
        ("Art Studio", "Explore painting, drawing, and sculpture techniques", 16),
        ("Drama Club", "Acting, theater productions, and script writing", 25),
        ("Debate Team", "Develop argumentation and public speaking skills", 14),
        ("Science Club", "Conduct experiments and explore scientific concepts", 18),
    ])
    def test_get_activities_has_correct_structure(self, client, activity_name, expected_description, expected_max):
        """
        AAA Test: Each activity has correct structure and required fields.
        
        Arrange: Use fresh client fixture; parametrize over all activities
        Act: Make GET request and extract specific activity
        Assert: Verify activity has all required fields with correct values
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        activity = data[activity_name]
        
        # Assert
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert activity["description"] == expected_description
        assert activity["max_participants"] == expected_max
        assert isinstance(activity["participants"], list)

    @pytest.mark.parametrize("activity_name,expected_participant_count", [
        ("Chess Club", 2),  # michael@mergington.edu, daniel@mergington.edu
        ("Programming Class", 2),  # emma@mergington.edu, sophia@mergington.edu
        ("Gym Class", 2),  # john@mergington.edu, olivia@mergington.edu
        ("Basketball Team", 1),  # james@mergington.edu
        ("Tennis Club", 2),  # alice@mergington.edu, ryan@mergington.edu
        ("Art Studio", 1),  # isabella@mergington.edu
        ("Drama Club", 2),  # lucas@mergington.edu, mia@mergington.edu
        ("Debate Team", 1),  # noah@mergington.edu
        ("Science Club", 2),  # ava@mergington.edu, ethan@mergington.edu
    ])
    def test_get_activities_shows_correct_participant_count(self, client, activity_name, expected_participant_count):
        """
        AAA Test: Each activity shows correct number of current participants.
        
        Arrange: Use fresh client fixture; parametrize over all activities with expected counts
        Act: Make GET request and extract participants list
        Assert: Verify participant count matches expected value for each activity
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        participants = data[activity_name]["participants"]
        
        # Assert
        assert len(participants) == expected_participant_count

    @pytest.mark.parametrize("activity_name,max_participants", [
        ("Chess Club", 12),
        ("Programming Class", 20),
        ("Gym Class", 30),
        ("Basketball Team", 15),
        ("Tennis Club", 20),
        ("Art Studio", 16),
        ("Drama Club", 25),
        ("Debate Team", 14),
        ("Science Club", 18),
    ])
    def test_get_activities_shows_correct_capacity_limits(self, client, activity_name, max_participants):
        """
        AAA Test: Each activity shows correct max_participants capacity limit.
        
        Arrange: Use fresh client fixture; parametrize over all activities with capacity limits
        Act: Make GET request and extract max_participants
        Assert: Verify max_participants matches expected capacity for each activity
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        activity = data[activity_name]
        
        # Assert
        assert activity["max_participants"] == max_participants

    def test_get_activities_response_is_json_dict(self, client):
        """
        AAA Test: GET /activities response is a JSON dictionary (not list or null).
        
        Arrange: Use fresh client fixture
        Act: Make GET request and parse response
        Assert: Verify response is a dictionary
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0
