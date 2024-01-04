from lib.models.__init__ import CONN, CURSOR


class User:
    def __init__(self, username, id=None):
        self.username = username
        self.id = id
        if id is not None:
            User.all[id] = self

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not isinstance(username, str) or not username:
            raise ValueError("username must be a non-empty string")
        self._username = username

    @classmethod
    def get_or_create(cls, username):
        # Check if the username already exists in the database
        CURSOR.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = CURSOR.fetchone()

        if existing_user:
            # If the user exists, return that user
            return cls(username=existing_user[1], id=existing_user[0])
        else:
            # If the user doesn't exist, create a new one and return it
            new_user = cls(username)
            new_user.save()
            return new_user

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
               username TEXT
           )
       """
        )
        conn.commit()

    @classmethod
    def drop_table(cls, conn, cursor):
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()

    @classmethod
    def instance_from_db(cls, id):
        CURSOR.execute("SELECT * FROM users WHERE id=?", (id,))
        user = CURSOR.fetchone()
        return cls(*user) if user else None

    # gets all users from the database but we dont want that. as user controls their instance.
    # @classmethod
    # def get_all(cls):
    #     CURSOR.execute("SELECT * FROM users")
    #     users = CURSOR.fetchall()
    #     return [cls(*user) for user in users]

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
        if self.id is None:
            CURSOR.execute("INSERT INTO users (username) VALUES (?)", (self.username,))
            self.id = CURSOR.lastrowid
            CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM users WHERE id=?", (self.id,))
        CONN.commit()
