import asyncio
import aiosqlite

DB_NAME = "users.db"


async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        result = await cursor.fetchall()
        await cursor.close()
        print("All users:")
        print(result)


async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        result = await cursor.fetchall()
        await cursor.close()
        print("Users older than 40:")
        print(result)


async def fetch_concurrently():
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
