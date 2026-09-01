"""
Pytest configuration and shared fixtures for backend API tests.

This module provides reusable fixtures that follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test client and reset app state
- Act: Tests execute endpoints
- Assert: Tests verify responses and state changes
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Initialize FastAPI TestClient with fresh app state.
    
    This fixture is run before each test (autouse=False) to provide a test client
    for making HTTP requests to the app. It resets the in-memory activities
    dictionary to a known clean state to ensure test isolation.
    
    Arrange phase: Prepares the test environment with a fresh TestClient
    and resets all activities to their initial state.
    
    Yields:
        TestClient: A test client for making requests to the FastAPI app
    """
    # Reset activities to initial state (Arrange)
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and practice sessions",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Tuesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["alice@mergington.edu", "ryan@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, theater productions, and script writing",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:45 PM",
            "max_participants": 14,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        }
    })
    
    # Provide test client to test
    return TestClient(app)


@pytest.fixture
def verify_activity_state():
    """
    Fixture: Helper to verify activity state after operations.
    
    This fixture provides a function to check the state of an activity's
    participants list after test operations. Used in Assert phase to verify
    that the app correctly modified the activity state.
    
    Assert phase: Helper for verifying that activities were modified correctly
    
    Yields:
        function: A helper function that takes (activity_name, expected_participants)
                  and verifies the actual participants match
    """
    def _verify(activity_name, expected_participants):
        """
        Verify that an activity has the expected participants.
        
        Args:
            activity_name (str): Name of the activity to check
            expected_participants (list): List of expected participant emails
            
        Returns:
            bool: True if participants match, False otherwise
        """
        if activity_name not in activities:
            return False
        return activities[activity_name]["participants"] == expected_participants
    
    return _verify
