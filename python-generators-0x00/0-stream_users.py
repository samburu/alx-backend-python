# 0-stream_users.py

import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def stream_users():
    """Generator that yields one row at a time from user_data table."""
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': os.getenv('DB_PASSWORD'),
        'port': 3306,
        'database': 'ALX_prodev'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    finally:
        try:
            cursor.fetchall()  # ensure all rows are read
        except:
            pass
        cursor.close()
        connection.close()

if __name__ == "__main__":
    from itertools import islice
    for user in islice(stream_users(), 6):
        print(user)
