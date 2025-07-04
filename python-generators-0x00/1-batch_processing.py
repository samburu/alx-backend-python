import os
from decimal import Decimal

import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),
    "port": 3306,
    "database": "ALX_prodev",
}


def stream_users_in_batches(batch_size):
    """Generator that yields user_data rows in batches."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """Processes batches and filters users older than 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            # Handle Decimal type
            age = user["age"]
            if isinstance(age, Decimal):
                age = int(age)
            if age > 25:
                print(user)


if __name__ == "__main__":
    batch_processing(50)
