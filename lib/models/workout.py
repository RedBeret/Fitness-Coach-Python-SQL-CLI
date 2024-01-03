from models.__init__ import CONN, CURSOR


class Workout:
    all = []

    def __init__(self, username, date, id=None, workout_duration=None, goal=None):
        self.username = username
        self.date = date
        self.id = id
        self.workout_duration = workout_duration
        self.goal = goal
        self.all[self.id] = self

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        elif not len(username) > 0:
            raise ValueError("Username cannot be empty")
        else:
            self._username = username

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if not isinstance(date, str):
            raise TypeError("Date must be a string")
        elif not len(date) > 0:
            raise ValueError("Date cannot be empty")
        else:
            self._date = date

    @property
    def workout_duration(self):
        # Fetch all exercises associated with the workout
        CURSOR.execute("SELECT * FROM workout_exercises WHERE workout_id=?", (self.id,))
        workout_exercises = CURSOR.fetchall()

        # Sum the durations of all exercises
        total_duration = sum(
            [exercise["duration_minutes"] for exercise in workout_exercises]
        )

        return total_duration

    @workout_duration.setter
    def workout_duration(self, workout_duration):
        if not isinstance(workout_duration, int):
            raise TypeError("Workout duration must be an integer")
        else:
            # Fetch all exercises related to the workout
            CURSOR.execute(
                "SELECT * FROM workout_exercises WHERE workout_id=?", (self.id,)
            )

            workout_exercises = CURSOR.fetchall()

        # Sum the durations of all exercises
        total_duration = sum(
            [exercise["duration_minutes"] for exercise in workout_exercises]
        )

        # Set the workout duration
        self._workout_duration = total_duration

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, goal):
        if not isinstance(goal, str):
            raise TypeError("Goal must be a string")
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
          CREATE TABLE IF NOT EXISTS workouts (
              id INTEGER PRIMARY KEY,
              username VARCHAR,
              date DATE,
              workout_duration INTEGER,
              goal VARCHAR
          )
          """
        )
        conn.commit()

    @classmethod
    def drop_table(cls, conn, cursor):
        cursor.execute("DROP TABLE IF EXISTS workouts")
        conn.commit()

    @classmethod
    def create(cls, username, date, workout_duration, goal):
        if not username or not date or not workout_duration or not goal:
            raise ValueError("All fields cannot be empty.")
        cls(username, date, workout_duration, goal).save()

    @classmethod
    def instance_from_db(cls, id):
        CURSOR.execute("SELECT * FROM workouts WHERE id=?", (id,))
        workout = CURSOR.fetchone()
        return cls(*workout) if workout else None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM workouts")
        workouts = CURSOR.fetchall()
        return [cls(*workout) for workout in workouts]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM workouts WHERE id=?", (id,))
        record = CURSOR.fetchone()
        return cls(*record) if record else None

    def save(self):
        CURSOR.execute(
            "INSERT INTO workouts (username, date, workout_duration, goal) VALUES (?, ?, ?, ?)",
            (self.username, self.date, self.workout_duration, self.goal),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self

    def update(self, username, date, workout_duration, goal):
        if not username or not date or not workout_duration or not goal:
            raise ValueError("All fields cannot be empty.")
        self.username = username
        self.date = date
        self.workout_duration = workout_duration
        self.goal = goal
        CURSOR.execute(
            "UPDATE workouts SET username=?, date=?, workout_duration=?, goal=? WHERE id=?",
            (self.username, self.date, self.workout_duration, self.goal, self.id),
        )
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM workouts WHERE id=?", (self.id,))
        CONN.commit()
        del self.__class__.all[self.id]
