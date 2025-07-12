import sqlite3


class ExecuteQuery:
    """Class to execute SQL queries using a SQLite database connection."""

    def __init__(self, query, params=None, db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Query connection closed.")


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (18,)

    with ExecuteQuery(query, params) as result:
        print("Query Result:", result)
