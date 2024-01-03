from models.__init__ import CONN, CURSOR


class Exercise:
    all = []

    def __init__(self, name, description, instructions, id=None):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.id = id
        self.all.append(self)

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

    @classmethod
    def create_table(cls, conn, cursor):
        cursor.execute(
            """
         CREATE TABLE IF NOT EXISTS exercises (
             id INTEGER PRIMARY KEY,
             name TEXT,
             description TEXT,
             instructions TEXT
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
            "INSERT INTO exercises (name, description, instructions) VALUES (?, ?, ?)",
            (self.name, self.description, self.instructions),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        self.__class__.ALL[self.id] = self

    def update(self, name, description):
        if not name or not description:
            raise ValueError("Name and Description cannot be empty.")
        self.name = name
        self.description = description
        CURSOR.execute(
            "UPDATE exercises SET name=?, description=? WHERE id=?",
            (self.name, self.description, self.id),
        )
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM exercises WHERE id=?", (self.id,))
        CONN.commit()
        del self.__class__.ALL[self.id]
