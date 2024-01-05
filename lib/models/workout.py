from datetime import date as dt_date
from datetime import datetime

current_date = datetime.today().strftime("%Y-%m-%d")

from .__init__ import CONN, CURSOR
from .exercise import Exercise


class Workout:
    all = {}

    def __init__(self, username, id=None, workout_duration=None, goal=None, date=None):
        self.username = username
        self.id = id
        self.workout_duration = workout_duration
        self.goal = goal
        self.date = date if date else str(dt_date.today())
        self.all[self.id] = self

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not (isinstance(username, str) and username.isalnum()) and not isinstance(
            username, int
        ):
            raise TypeError(
                "Username must be a string containing alphanumeric characters or an integer"
            )
        else:
            self._username = str(username)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if not (isinstance(date, str) and len(date) > 0):
            raise ValueError("Date must be a non-empty string")
        else:
            self._date = str(date)

    @property
    def workout_duration(self):
        # Fetch all exercises associated with the workout
        CURSOR.execute(
            "SELECT exercises.duration_minutes FROM workout_exercises INNER JOIN exercises ON workout_exercises.exercise_id = exercises.id WHERE workout_exercises.workout_id=?",
            (self.id,),
        )
        workout_exercises = CURSOR.fetchall()
        # Sum the durations of all exercises
        total_duration = sum(exercise[0] for exercise in workout_exercises)
        return total_duration

    @workout_duration.setter
    def workout_duration(self, workout_duration):
        if not isinstance(workout_duration, int):
            raise TypeError("Workout duration must be an integer")
        else:
            # Fetch all exercises related to the workout
            CURSOR.execute(
                """
        SELECT exercises.duration_minutes
        FROM workout_exercises
        JOIN exercises ON workout_exercises.exercise_id = exercises.id
        WHERE workout_exercises.workout_id=?
        """,
                (self.id,),
            )

        workout_exercises = CURSOR.fetchall()
        # Sum the durations of all exercises
        total_duration = sum(exercise[0] for exercise in workout_exercises)
        return total_duration

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, goal):
        if not isinstance(goal, str):
            raise TypeError("Goal must be a string")
        elif not goal:
            raise ValueError("Goal cannot be empty")
        else:
            self._goal = goal

    def __repr__(self):
        return f"<Workout {self.id}>"

    def __str__(self):
        return f"Workout ID: {self.id}, Date: {self.date}, Username: {self.username}, Workout Duration: {self.workout_duration}, Goal: {self.goal}"

    @classmethod
    def create_table(cls, conn, cursor):
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS user_workouts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        duration INTEGER NOT NULL,
        goal VARCHAR NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        )

    @classmethod
    def drop_table(cls, conn, cursor):
        cursor.execute("DROP TABLE IF EXISTS user_workouts")
        conn.commit()

    @classmethod
    def create(cls, username, workout_duration, goal, date=None):
        if not date:
            date = date.today().isoformat()

        if not username or not workout_duration or not goal:
            raise ValueError("Username, workout duration, and goal cannot be empty.")

        workout = cls(
            username=username, date=date, workout_duration=workout_duration, goal=goal
        )
        workout.save()
        return workout

    @classmethod
    def instance_from_db(cls, id):
        CURSOR.execute("SELECT * FROM user_workouts WHERE id=?", (id,))
        workout = CURSOR.fetchone()
        return cls(*workout) if workout else None

    @classmethod
    def get_all(cls, username):
        CURSOR.execute(
            """
            SELECT user_workouts.id, user_workouts.date, user_workouts.duration, user_workouts.goal
            FROM user_workouts
            JOIN users ON user_workouts.user_id = users.id
            WHERE users.username = ?
            """,
            (username,),
        )
        rows = CURSOR.fetchall()
        return [
            cls(username, id=row[0], date=row[1], workout_duration=row[2], goal=row[3])
            for row in rows
        ]

    @classmethod
    def get_exercises(cls, workout_id):
        CURSOR.execute(
            """
            SELECT e.id, e.name, e.sets, e.reps_per_set, e.duration_minutes, e.muscle_group 
            FROM workout_exercises we
            JOIN exercises e ON we.exercise_id = e.id 
            WHERE we.workout_id = ?
        """,
            (workout_id,),
        )
        return [Exercise(*row) for row in CURSOR.fetchall()]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM user_workouts WHERE id=?", (id,))
        record = CURSOR.fetchone()
        return cls(*record) if record else None

    def save(self):
        try:
            if self.id is None:
                CURSOR.execute(
                    """
                        INSERT INTO user_workouts (user_id, date, duration, goal)
                        VALUES ((SELECT id FROM users WHERE username = ?), ?, ?, ?)
                        """,
                    (self.username, self.date, self.workout_duration, self.goal),
                )
                CONN.commit()
                self.id = CURSOR.lastrowid
                self.__class__.all[self.id] = self
            else:
                # If the workout already has an ID, update the record
                CURSOR.execute(
                    """
                        UPDATE user_workouts SET date=?, duration=?, goal=? WHERE id=?
                        """,
                    (self.date, self.workout_duration, self.goal, self.id),
                )
                CONN.commit()
        except sqlite3.Error as database_error:
            print(f"An error occurred while saving the workout: {database_error}")

    @classmethod
    def delete_by_id(cls, workout_id):
        CURSOR.execute(
            "DELETE FROM workout_exercises WHERE workout_id = ?", (workout_id,)
        )
        CURSOR.execute("DELETE FROM user_workouts WHERE id = ?", (workout_id,))
        CONN.commit()
