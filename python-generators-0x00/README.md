# Python Generators: Streaming SQL Data

This project demonstrates how to use Python generators to efficiently stream rows from a MySQL database one by one.


##  Objective

- Set up a MySQL database `ALX_prodev`.
- Create a table `user_data` with fields:
  - `user_id` (UUID, PK, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populate the table from `user_data.csv`.
- Use a Python generator to stream rows one-by-one.

## seed.py Functionalities

- `connect_db()`
  Connects to MySQL (root connection, not yet selecting a database)

- `create_database(connection)`
  Creates the database `ALX_prodev` if it does not already exist

- `connect_to_prodev()`
  Connects to the `ALX_prodev` database

- `create_table(connection)`
  Creates the `user_data` table with required fields and an index

- `insert_data(connection, csv_file)`
  Loads data from a CSV file into the table


## How to Run

Make sure you have the following:

- MySQL installed and running
- `mysql-connector-python` installed via pip:
  ```
  pip install mysql-connector-python python-dotenv
  ```

- `.env` file with database credentials:
  ```
  DB_PASSWORD=your_password
  ```

Then run:

```bash
python python-generators-0x00/seed.py
```
