from models.__init__ import CONN, CURSOR


class Exercise:
    all = []

    def __init__(
        self,
        name,
        description,
        instructions,
        muscle_group,
        sets,
        reps_per_set,
        duration_minutes,
        id=None,
    ):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps_per_set = reps_per_set
        self.duration_minutes = duration_minutes
        self.id = id
        self.all[self.id] = self

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

    def __repr__(self):
        return f"<Exercise {self.name}>"

    def __str__(self):
        return f"{self.name}: {self.description}"

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
    def create(cls, name, description):
        if not name or not description:
            raise ValueError("Name and Description cannot be empty.")
        cls(name, description).save()

    @classmethod
    def instance_from_db(cls, id):
        CURSOR.execute("SELECT * FROM exercises WHERE id=?", (id,))
        exercise = CURSOR.fetchone()
        return cls(*exercise) if exercise else None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM exercises")
        exercises = CURSOR.fetchall()
        return [cls(*exercise) for exercise in exercises]

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

    def save(self):
        CURSOR.execute(
            "INSERT INTO exercises (name, description, instructions, muscle_group, sets, reps_per_set, duration_minutes) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
        self.__class__.ALL[self.id] = self

    def update(
        self, name, description, muscle_group, sets, reps_per_set, duration_minutes
    ):
        if (
            not name
            or not description
            or not muscle_group
            or not sets
            or not reps_per_set
            or not duration_minutes
        ):
            raise ValueError("All fields cannot be empty.")
        self.name = name
        self.description = description
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps_per_set = reps_per_set
        self.duration_minutes = duration_minutes

    CURSOR.execute(
        "UPDATE exercises SET name=?, description=?, muscle_group=?, sets=?, reps_per_set=?, duration_minutes=? WHERE id=?",
        (
            self.name,
            self.description,
            self.muscle_group,
            self.sets,
            self.reps_per_set,
            self.duration_minutes,
            self.id,
        ),
    )
    CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM exercises WHERE id=?", (self.id,))
        CONN.commit()
        del self.__class__.ALL[self.id]
