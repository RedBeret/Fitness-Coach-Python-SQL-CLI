from models.__init__ import CONN, CURSOR


class User:
    all = []

    def __init__(self, username, id=None):
        self.username = username
        self.id = id
        self.all.append(self)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        elif not len(username) > 0:
            raise ValueError("username cannot be empty")
        else:
            # Check if the username already exists in the database
            CURSOR.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = CURSOR.fetchone()
            if existing_user is not None:
                raise ValueError("This username is already taken.")
            else:
                self._username = username

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return f"{self.username}"

    @classmethod
    def create_table(cls, conn, cursor):
        cursor.execute(
            """
           CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               full_name TEXT
           )
       """
        )
        conn.commit()

    @classmethod
    def drop_table(cls, conn, cursor):
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()

    @classmethod
    def create(cls, username):
        if not username:
            raise ValueError("Username cannot be empty.")
        cls(username).save()

    @classmethod
    def instance_from_db(cls, id):
        CURSOR.execute("SELECT * FROM users WHERE id=?", (id,))
        user = CURSOR.fetchone()
        return cls(*user) if user else None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM users")
        users = CURSOR.fetchall()
        return [cls(*user) for user in users]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM users WHERE id=?", (id,))
        record = CURSOR.fetchone()
        return cls(*record) if record else None

    @classmethod
    def find_by_name(cls, username):
        CURSOR.execute("SELECT * FROM users WHERE username=?", (username,))
        record = CURSOR.fetchone()
        return cls(*record) if record else None

    def save(self):
        CURSOR.execute("INSERT INTO users (username) VALUES (?)", (self.username,))
        CONN.commit()
        self.id = CURSOR.lastrowid
        self.__class__.ALL[self.id] = self

    def update(self, username):
        if not username:
            raise ValueError("Username cannot be empty.")
        self.username = username
        CURSOR.execute(
            "UPDATE users SET username=? WHERE id=?", (self.username, self.id)
        )
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM users WHERE id=?", (self.id,))
        CONN.commit()
        del self.__class__.ALL[self.id]
