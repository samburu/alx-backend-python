import functools
import sqlite3
import time


def with_db_connection(func):
    """Decorator that opens and closes a database connection."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function on failure for transient errors."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[WARNING] Attempt {attempt} failed: {e}")
                    time.sleep(delay)
            print("[ERROR] All retry attempts failed.")
            raise last_exception

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
