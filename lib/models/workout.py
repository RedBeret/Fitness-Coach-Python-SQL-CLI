from models.__init__ import CONN, CURSOR


class Workout:
    all = []

    def __init__(self, user, date, id=None):
        self.user = user
        self.date = date
        self.id = id
        self.all.append(self)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise TypeError("user must be an instance of User")
        else:
            self._user = user

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

    def __repr__(self):
        return f"<Workout {self.id}>"

    def __str__(self):
        return f"Workout ID: {self.id}, Date: {self.date}"

    @classmethod
    def create_table(cls, conn, cursor):
        cursor.execute(
            """
           CREATE TABLE IF NOT EXISTS workouts (
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               date TEXT
           )
           """
        )
        conn.commit()

    @classmethod
    def drop_table(cls, conn, cursor):
        cursor.execute("DROP TABLE IF EXISTS workouts")
        conn.commit()

    @classmethod
    def create(cls, user_id, date):
        if not user_id or not date:
            raise ValueError("User ID and Date cannot be empty.")
        cls(user_id, date).save()

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
            "INSERT INTO workouts (user_id, date) VALUES (?, ?)",
            (self.user_id, self.date),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        self.__class__.ALL[self.id] = self

    def update(self, user_id, date):
        if not user_id or not date:
            raise ValueError("User ID and Date cannot be empty.")
        self.user_id = user_id
        self.date = date
        CURSOR.execute(
            "UPDATE workouts SET user_id=?, date=? WHERE id=?",
            (self.user_id, self.date, self.id),
        )
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM workouts WHERE id=?", (self.id,))
        CONN.commit()
        del self.__class__.ALL[self.id]
