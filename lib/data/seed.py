import sqlite3

from exercise_database import exercises

# Connect to the SQLite database
conn = sqlite3.connect("lib/data/workout_plans.db")
cursor = conn.cursor()

# SQL statements to create tables
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username VARCHAR NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS exercises (
  id INTEGER PRIMARY KEY,
  name VARCHAR NOT NULL,
  description VARCHAR NOT NULL,
  instructions VARCHAR NOT NULL,
  muscle_group VARCHAR NOT NULL,
  sets INTEGER NOT NULL,
  reps_per_set INTEGER NOT NULL,
  duration_minutes INTEGER NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS user_workouts (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  date DATE NOT NULL,
  duration INTEGER NOT NULL,
  goal VARCHAR NOT NULL,
  exercises TEXT,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS workout_exercises (
  workout_id INTEGER NOT NULL,
  exercise_id INTEGER NOT NULL,
  PRIMARY KEY (workout_id, exercise_id),
  FOREIGN KEY (workout_id) REFERENCES user_workouts (id),
  FOREIGN KEY (exercise_id) REFERENCES exercises (id)
);
"""
)

# Insert seed data for exercises
for exercise in exercises:
    cursor.execute(
        """
        INSERT INTO exercises (name, description, instructions, muscle_group, sets, reps_per_set, duration_minutes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            exercise["name"],
            exercise["description"],
            exercise["instructions"],
            exercise["muscle_group"],
            exercise["sets"],
            exercise["reps_per_set"],
            exercise["duration_minutes"],
        ),
    )

# Seed data for users
users = [{"username": "noname19"}, {"username": "noname20"}]

# Insert seed data for users
for user in users:
    cursor.execute(
        """
        INSERT INTO users (username) VALUES (?)
        """,
        (user["username"],),
    )

# Seed data for workouts (example workouts)
workouts = [
    {
        "user_id": 1,
        "date": "2024-01-03",
        "workout_duration": 60,
        "goal": "Strength Training",
        "exercises": "[1, 2, 3]",
    },
    {
        "user_id": 2,
        "date": "2024-01-04",
        "workout_duration": 45,
        "goal": "Cardio",
        "exercises": "[4, 5, 6]",
    },
]

# Insert seed data for user workouts
for workout in workouts:
    cursor.execute(
        """
    INSERT INTO user_workouts (user_id, date, duration, goal, exercises) VALUES (?, ?, ?, ?, ?)
    """,
        (
            workout["user_id"],
            workout["date"],
            workout["workout_duration"],
            workout["goal"],
            workout["exercises"],
        ),
    )

conn.commit()
conn.close()

print("Database 'workout_plans.db' has been seeded successfully.")
