import sqlite3

from lib.models.__init__ import CONN, CURSOR


class Exercise:
    all = {}

    def __init__(
        self,
        id=None,
        name=None,
        description=None,
        instructions=None,
        muscle_group=None,
        sets=None,
        reps_per_set=None,
        duration_minutes=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.instructions = instructions
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps_per_set = reps_per_set
        self.duration_minutes = duration_minutes

    def __repr__(self):
        return f"<Exercise {self.name}>"

    def __str__(self):
        return f"{self.name}: {self.description}"

    # Class Properties

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Exercise name must be a string")
        elif not len(name) > 0:
            raise ValueError("Exercise name cannot be empty")
        else:
            self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        elif not len(description) > 0:
            raise ValueError("Description cannot be empty")
        else:
            self._description = description

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, instructions):
        if not isinstance(instructions, str):
            raise TypeError("Instructions must be a string")
        elif not len(instructions) > 0:
            raise ValueError("Instructions cannot be empty")
        else:
            self._instructions = instructions

    @property
    def muscle_group(self):
        return self._muscle_group

    @muscle_group.setter
    def muscle_group(self, muscle_group):
        if not isinstance(muscle_group, str):
            raise TypeError("Muscle group must be a string")
        elif not len(muscle_group) > 0:
            raise ValueError("Muscle group cannot be empty")
        else:
            self._muscle_group = muscle_group

    @property
    def sets(self):
        return self._sets

    @sets.setter
    def sets(self, sets):
        if not isinstance(sets, int):
            raise TypeError("Sets must be an integer")
        elif sets < 0:
            raise ValueError("Sets cannot be negative")
        else:
            self._sets = sets

    @property
    def reps_per_set(self):
        return self._reps_per_set

    @reps_per_set.setter
    def reps_per_set(self, reps_per_set):
        if not isinstance(reps_per_set, int):
            raise TypeError("Reps per set must be an integer")
        elif reps_per_set < 0:
            raise ValueError("Reps per set cannot be negative")
        else:
            self._reps_per_set = reps_per_set

    @property
    def duration_minutes(self):
        return self._duration_minutes

    @duration_minutes.setter
    def duration_minutes(self, duration_minutes):
        if not isinstance(duration_minutes, int):
            raise TypeError("Duration minutes must be an integer")
        elif duration_minutes < 0:
            raise ValueError("Duration minutes cannot be negative")
        else:
            self._duration_minutes = duration_minutes

    # Class Methods

    @classmethod
    def create_table(cls, conn, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                instructions TEXT,
                muscle_group TEXT,
                sets INTEGER,
                reps_per_set INTEGER,
                duration_minutes INTEGER
            )
        """
        )
        conn.commit()

    @classmethod
    def drop_table(cls, conn, cursor):
        cursor.execute("DROP TABLE IF EXISTS exercises")
        conn.commit()

    @classmethod
    def create(
        cls,
        name,
        description,
        instructions,
        muscle_group,
        sets,
        reps_per_set,
        duration_minutes,
    ):
        exercise = cls(
            name=name,
            description=description,
            instructions=instructions,
            muscle_group=muscle_group,
            sets=sets,
            reps_per_set=reps_per_set,
            duration_minutes=duration_minutes,
        )
        exercise.save()
        return exercise

    @classmethod
    def instance_from_db(cls, id):
        CURSOR.execute("SELECT * FROM exercises WHERE id=?", (id,))
        exercise = CURSOR.fetchone()
        return cls(*exercise) if exercise else None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM exercises")
        records = CURSOR.fetchall()
        return [cls(*record) for record in records]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM exercises WHERE id=?", (id,))
        record = CURSOR.fetchone()
        return cls(*record) if record else None

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM exercises WHERE name=?", (name,))
        record = CURSOR.fetchone()
        return cls(*record) if record else None

    # CRUD Operations

    def save(self):
        try:
            if self.id is None:
                CURSOR.execute(
                    """
                        INSERT INTO exercises (name, description, instructions, muscle_group, sets, reps_per_set, duration_minutes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                    (
                        self.name,
                        self.description,
                        self.instructions,
                        self.muscle_group,
                        self.sets,
                        self.reps_per_set,
                        self.duration_minutes,
                    ),
                )
                CONN.commit()
                self.id = CURSOR.lastrowid
            else:
                self.update()
        except sqlite3.Error as database_error:
            print(f"An error occurred while saving the exercise: {database_error}")

    def update(self):
        try:
            CURSOR.execute(
                """
                    UPDATE exercises SET name=?, description=?, instructions=?, muscle_group=?, sets=?, reps_per_set=?, duration_minutes=?
                    WHERE id=?
                    """,
                (
                    self.name,
                    self.description,
                    self.instructions,
                    self.muscle_group,
                    self.sets,
                    self.reps_per_set,
                    self.duration_minutes,
                    self.id,
                ),
            )
            CONN.commit()
        except sqlite3.Error as database_error:
            print(f"An error occurred while updating the exercise: {database_error}")

    def delete(self):
        try:
            CURSOR.execute("DELETE FROM exercises WHERE id=?", (self.id,))
            CONN.commit()
        except sqlite3.Error as database_error:
            print(f"An error occurred while deleting the exercise: {database_error}")
