import sqlite3


class Database:
    def __init__(self):
        self.filename = "task.db"
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT,
                location TEXT,
                timestamp TEXT,
                status TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                recipient_email TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
        )
        self.connection.commit()

    def add_task(self, task, location, timestamp,status, user_id):
        self.cursor.execute(
            "INSERT INTO tasks (task, location, timestamp,status, user_id) VALUES (?, ?, ?, ?, ?)",
            (task, location, timestamp,status, user_id)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def add_user(self, username, password):
        # Check if the user already exists
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            return existing_user[0]
        
        # Add the new user
        self.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    
    def fetch_tasks_for_user(self, user_id):
        self.cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def fetch_one_task(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return self.cursor.fetchone()
    
    def update_task(self, task_id, new_task, new_location, new_timestamp,new_status):
        self.cursor.execute(
            "UPDATE tasks SET task = ?, location = ?, timestamp = ?, status = ? WHERE id = ?",
            (new_task, new_location, new_timestamp,new_status, task_id)
        )
        self.connection.commit()

    def delete_task(self, task_id, user_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id,user_id))
        self.connection.commit()

    def upsert_user_settings(self, user_id, recipient_email):
        self.cursor.execute(
            """
            INSERT INTO user_settings (user_id, recipient_email)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET recipient_email = excluded.recipient_email
            """,
            (user_id, recipient_email)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    def get_user_settings(self, user_id):
        self.cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        settings = self.cursor.fetchone()
        if settings:
            return settings
        return None

    def close(self):
        self.connection.close()

