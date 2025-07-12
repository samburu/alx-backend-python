import sqlite3


class DatabaseConnection:
    """Custom context manager for handling SQLite DB connections."""

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")


# Use the context manager to query the users table

if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Users:", users)
