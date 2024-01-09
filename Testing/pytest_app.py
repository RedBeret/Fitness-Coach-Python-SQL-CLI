import pytest
import sqlite3
from lib.models.user import User
from lib.models.exercise import Exercise
from lib.models.workout import Workout

@pytest.fixture(scope="module")
def db():
    """Set up an in-memory database for testing."""
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    User.create_table(connection, cursor)
    Exercise.create_table(connection, cursor)
    Workout.create_table(connection, cursor)
    yield cursor
    connection.close()

# User Model Tests
def test_create_user(db):
    """User Model: Creating a user should assign an ID."""
    user = User(username="testuser")
    user.save()
    assert user.id is not None


# Exercise Model Tests
def test_create_exercise(db):
    """Exercise Model: Creating an exercise should assign an ID."""
    exercise = Exercise.create(name="Bicycles", description="test description", instructions="test instructions", muscle_group="Core", sets=3, reps_per_set=10, duration_minutes=5)
    assert exercise.id is not None

def test_find_exercise_by_name(db):
    """Exercise Model: Finding an exercise by name should return the correct exercise."""
    name = "Bicycles"
    found_exercise = Exercise.find_by_name(name)
    assert found_exercise.name == name

def test_update_exercise(db):
    """Exercise Model: Updating exercise's sets, reps, and duration should reflect changes."""
    exercise = Exercise.find_by_name("Bicycles")
    exercise.sets = 4
    exercise.reps_per_set = 15
    exercise.duration_minutes = 10
    exercise.save()
    updated_exercise = Exercise.find_by_name("Bicycles")
    assert updated_exercise.sets == 4 and updated_exercise.reps_per_set == 15 and updated_exercise.duration_minutes == 10

def test_list_all_exercises(db):
    """Exercise Model: Listing all exercises should return a list of exercises."""
    exercises = Exercise.get_all()
    assert len(exercises) > 0

def test_delete_exercise(db):
    """Exercise Model: Deleting an exercise should remove it from the database."""
    exercise = Exercise.find_by_name("Bicycles")
    exercise_id = exercise.id
    exercise.delete()
    deleted_exercise = Exercise.find_by_id(exercise_id)
    assert deleted_exercise is None

# Workout Model Tests
def test_create_workout(db):
    """Workout Model: Creating a workout should assign an ID."""
    user = User(username="newuser")
    user.save()
    workout = Workout.create(username=user.username, workout_duration=30, goal="Strength")
    assert workout.id is not None

