import decimal
from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields one user age at a time.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]
    cursor.close()
    conn.close()


def compute_average_age():
    """
    Uses the generator to compute the average age without loading all into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        # In case the DB returns Decimal, convert to int/float
        total_age += float(age)
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
