"""
Tests for POST /signup and DELETE /unregister endpoints.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Use fixtures to set up the test client and reset app state
- Act: Make POST/DELETE requests to signup/unregister endpoints
- Assert: Verify response status, content, and app state changes
"""

import pytest
from app import activities


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "alex@mergington.edu"),
        ("Programming Class", "jordan@mergington.edu"),
        ("Basketball Team", "sam@mergington.edu"),
        ("Tennis Club", "casey@mergington.edu"),
    ])
    def test_signup_success_adds_participant(self, client, activity_name, email):
        """
        AAA Test: Successful signup adds participant to activity.
        
        Arrange: Use fresh client and parametrize activity/email combinations
        Act: Make POST request to signup endpoint
        Assert: Verify status code is 200, participant added to activity
        """
        # Arrange: Get initial participant count
        initial_count = len(activities[activity_name]["participants"])
        
        # Act: Signup for activity
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert: Verify success and participant added
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1
        assert "signed up" in response.json()["message"].lower()

    def test_signup_returns_success_message(self, client):
        """
        AAA Test: Successful signup returns appropriate success message.
        
        Arrange: Use fresh client fixture
        Act: Make successful signup POST request
        Assert: Verify response contains success message with participant email and activity name
        """
        # Act
        response = client.post("/activities/Chess Club/signup?email=test@example.com")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "test@example.com" in data["message"]
        assert "Chess Club" in data["message"]

    @pytest.mark.parametrize("activity_name,email,expected_error", [
        ("Chess Club", "michael@mergington.edu", "already signed up"),
        ("Chess Club", "daniel@mergington.edu", "already signed up"),
        ("Programming Class", "emma@mergington.edu", "already signed up"),
        ("Gym Class", "john@mergington.edu", "already signed up"),
    ])
    def test_signup_duplicate_email_returns_400(self, client, activity_name, email, expected_error):
        """
        AAA Test: Duplicate signup attempt returns 400 error with appropriate message.
        
        Arrange: Use fresh client; parametrize duplicate participant scenarios
        Act: Attempt to signup with email already enrolled in activity
        Assert: Verify status code is 400 and error message mentions duplicate signup
        """
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert expected_error.lower() in response.json()["detail"].lower()

    def test_signup_invalid_activity_returns_404(self, client):
        """
        AAA Test: Signup to non-existent activity returns 404 error.
        
        Arrange: Use fresh client fixture
        Act: Attempt signup to activity that doesn't exist
        Assert: Verify status code is 404 and error indicates activity not found
        """
        # Act
        response = client.post("/activities/Nonexistent Activity/signup?email=test@example.com")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_at_capacity_returns_400(self, client):
        """
        AAA Test: Signup to full activity returns 400 error.
        
        Arrange: Set activity to max capacity, then attempt signup
        Act: Make POST request to signup for activity at capacity
        Assert: Verify status code is 400 and error indicates activity is full
        """
        # Arrange: Fill activity to max capacity
        max_cap = activities["Basketball Team"]["max_participants"]
        activities["Basketball Team"]["participants"] = [
            f"participant{i}@mergington.edu" for i in range(max_cap)
        ]
        
        # Act
        response = client.post("/activities/Basketball Team/signup?email=newstudent@mergington.edu")
        
        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()
        assert "newstudent@mergington.edu" not in activities["Basketball Team"]["participants"]

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "new1@mergington.edu"),
        ("Tennis Club", "new2@mergington.edu"),
        ("Drama Club", "new3@mergington.edu"),
    ])
    def test_signup_below_capacity_succeeds(self, client, activity_name, email):
        """
        AAA Test: Signup succeeds when activity is below max capacity.
        
        Arrange: Parametrize different activities with available spots
        Act: Make POST request to signup for activity below capacity
        Assert: Verify successful signup and participant count increases
        """
        # Arrange
        activity = activities[activity_name]
        initial_count = len(activity["participants"])
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email in activity["participants"]
        assert len(activity["participants"]) == initial_count + 1


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_removes_participant(self, client, verify_activity_state):
        """
        AAA Test: Unregister removes participant from activity.
        
        Arrange: Use fresh client and verify_activity_state helper
        Act: Make DELETE request to unregister participant
        Assert: Verify status code is 200, participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_participants = activities[activity_name]["participants"].copy()
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == len(initial_participants) - 1
        assert "unregistered" in response.json()["message"].lower()

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "daniel@mergington.edu"),
        ("Programming Class", "emma@mergington.edu"),
        ("Gym Class", "john@mergington.edu"),
        ("Science Club", "ava@mergington.edu"),
    ])
    def test_unregister_success_removes_correct_participant(self, client, activity_name, email):
        """
        AAA Test: Unregister removes correct participant from activity.
        
        Arrange: Parametrize different activity/participant combinations
        Act: Make DELETE request to unregister
        Assert: Verify participant removed and others remain in activity
        """
        # Arrange
        original_participants = activities[activity_name]["participants"].copy()
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        # Verify other participants still in activity
        for other_email in original_participants:
            if other_email != email:
                assert other_email in activities[activity_name]["participants"]

    def test_unregister_invalid_activity_returns_404(self, client):
        """
        AAA Test: Unregister from non-existent activity returns 404 error.
        
        Arrange: Use fresh client fixture
        Act: Attempt to unregister from activity that doesn't exist
        Assert: Verify status code is 404 and error indicates activity not found
        """
        # Act
        response = client.delete("/activities/Nonexistent Activity/unregister?email=test@example.com")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "notinactivity@mergington.edu"),
        ("Programming Class", "noparticipant@mergington.edu"),
        ("Tennis Club", "notmember@mergington.edu"),
    ])
    def test_unregister_email_not_in_activity_returns_404(self, client, activity_name, email):
        """
        AAA Test: Unregister attempt for non-participant returns 404 error.
        
        Arrange: Parametrize activities with emails not enrolled
        Act: Attempt to unregister email not in activity participants
        Assert: Verify status code is 404 and error indicates student not found in activity
        """
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_returns_success_message(self, client):
        """
        AAA Test: Successful unregister returns appropriate success message.
        
        Arrange: Use fresh client fixture
        Act: Make successful unregister DELETE request
        Assert: Verify response contains success message with email and activity name
        """
        # Act
        response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_unregister_twice_second_fails(self, client):
        """
        AAA Test: Second unregister of same participant fails with 404.
        
        Arrange: Use fresh client, unregister a participant once
        Act: Attempt to unregister same participant again
        Assert: Verify first unregister succeeds, second returns 404
        """
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"
        
        # Act: First unregister
        response1 = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response1.status_code == 200
        
        # Act: Second unregister (should fail)
        response2 = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response2.status_code == 404

