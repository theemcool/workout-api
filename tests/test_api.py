
import os
import sys
import pytest

# Add the project root to Python's module search path.
# This allows tests to import app.py and config.py.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import create_app
from config import db


@pytest.fixture
def client():
    # Create a separate test application using an in-memory database.
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        # Create database tables before running each test.
        db.create_all()

        with app.test_client() as client:
            yield client

        # Clean up the test database after each test.
        db.session.remove()
        db.drop_all()


def test_homepage(client):
    # Check that the API homepage responds successfully.
    response = client.get("/")
    assert response.status_code == 200


def test_create_workout(client):
    # Check that a workout can be created.
    response = client.post("/workouts/", json={
        "name": "Leg Day",
        "description": "Lower-body strength training",
        "date": "2026-10-30"
    })

    assert response.status_code == 201


def test_create_workout_without_name(client):
    # Check that a workout without a name is rejected.
    response = client.post("/workouts/", json={
        "description": "Lower-body strength training",
        "date": "2026-10-30"
    })

    assert response.status_code == 400


def test_get_workouts(client):
    # Check that the API can retrieve the workout collection.
    response = client.get("/workouts/")
    assert response.status_code == 200


def test_delete_workout(client):
    # Create a workout first so there is a record to delete.
    create_response = client.post("/workouts/", json={
        "name": "Leg Day",
        "description": "Lower-body training",
        "date": "2026-10-30"
    })

    workout_id = create_response.get_json()["id"]

    # Delete the newly created workout.
    response = client.delete(f"/workouts/{workout_id}")
    assert response.status_code == 200


def test_create_exercise(client):
    # Check that a new exercise can be created.
    response = client.post("/exercises/", json={
        "name": "Squats",
        "description": "Lower-body strength exercise",
        "muscle_group": "Legs"
    })

    assert response.status_code == 201


def test_duplicate_exercise(client):
    # Create the first exercise.
    exercise_data = {
        "name": "Squats",
        "description": "Lower-body strength exercise",
        "muscle_group": "Legs"
    }

    client.post("/exercises/", json=exercise_data)

    # Attempt to create another exercise with the same name.
    response = client.post("/exercises/", json=exercise_data)

    assert response.status_code == 409


def test_get_exercises(client):
    # Check that the API can retrieve all exercises.
    response = client.get("/exercises/")
    assert response.status_code == 200


def test_assign_exercise_to_workout(client):
    # Create a workout.
    workout_response = client.post("/workouts/", json={
        "name": "Leg Day",
        "description": "Lower-body strength training",
        "date": "2026-10-30"
    })

    # Create an exercise.
    exercise_response = client.post("/exercises/", json={
        "name": "Squats",
        "description": "Lower-body strength exercise",
        "muscle_group": "Legs"
    })

    workout_id = workout_response.get_json()["id"]
    exercise_id = exercise_response.get_json()["id"]

    # Assign the exercise to the workout.
    response = client.post("/workout-exercises/", json={
        "workout_id": workout_id,
        "exercise_id": exercise_id,
        "sets": 3,
        "reps": 12
    })

    assert response.status_code == 201


def test_assignment_with_missing_workout(client):
    # Create an exercise but do not create a workout.
    exercise_response = client.post("/exercises/", json={
        "name": "Squats",
        "description": "Lower-body strength exercise",
        "muscle_group": "Legs"
    })

    exercise_id = exercise_response.get_json()["id"]

    # Attempt to assign the exercise to a nonexistent workout.
    response = client.post("/workout-exercises/", json={
        "workout_id": 999,
        "exercise_id": exercise_id,
        "sets": 3,
        "reps": 12
    })

    assert response.status_code == 404
