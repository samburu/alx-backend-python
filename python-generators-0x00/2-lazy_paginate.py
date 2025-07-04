#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily paginates through user_data table.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


if __name__ == "__main__":
    for page in lazy_pagination(100):
        for user in page:
            print(user)
