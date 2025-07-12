import functools
import sqlite3
import time

query_cache = {}


def with_db_connection(func):
    """Decorator that opens and closes DB connection."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


def cache_query(func):
    """Decorator that caches results of DB queries based on query string."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[DB] Query result cached.")
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call — will hit DB and cache result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — will return cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
