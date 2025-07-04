import csv
import os
import uuid

import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),
    "port": 3306,
}

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def connect_db():
    """Connect to MySQL server (no specific database)"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        connection.commit()
        cursor.close()
        print(f"Database {DB_NAME} created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to {DB_NAME}: {err}")
        return None


def create_table(connection):
    """Create user_data table with specified fields"""
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            );
        """
        )
        cursor.execute("CREATE INDEX idx_user_id ON user_data(user_id)")

        connection.commit()
        cursor.close()
        print(f"Table {TABLE_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")


def insert_data(connection, csv_path):
    """Insert data from CSV into user_data table if not already present"""
    try:
        cursor = connection.cursor()
        with open(csv_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row.get("user_id") or str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]
                cursor.execute(
                    f"""
                    SELECT user_id FROM {TABLE_NAME} WHERE user_id = %s
                """,
                    (user_id,),
                )
                if not cursor.fetchone():
                    cursor.execute(
                        f"""
                        INSERT INTO {TABLE_NAME}(user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """,
                        (user_id, name, email, age),
                    )
        connection.commit()
        cursor.close()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to insert data: {err}")
    except FileNotFoundError:
        print(f"CSV file {csv_path} not found.")


def main():
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Initial connection successful")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, "user_data.csv")

            cursor = connection.cursor()
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';"
            )
            if cursor.fetchone():
                print("Database ALX_prodev is present")

            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            for row in cursor.fetchall():
                print(row)
            cursor.close()


if __name__ == "__main__":
    main()
