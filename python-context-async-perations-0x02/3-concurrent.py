import asyncio

import aiosqlite

DB_NAME = "users.db"


async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("\n[All Users]")
            for user in users:
                print(user)


async def async_fetch_older_users(age):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (age,)) as cursor:
            users = await cursor.fetchall()
            print(f"\n[Users older than {age}]")
            for user in users:
                print(user)


async def fetch_concurrently():
    await asyncio.gather(async_fetch_users(), async_fetch_older_users(40))


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
