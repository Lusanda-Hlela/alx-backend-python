import asyncio
import aiosqlite

DB_NAME = "users.db"


async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        result = await cursor.fetchall()
        await cursor.close()
        return result


async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        result = await cursor.fetchall()
        await cursor.close()
        return result


async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )
    print("All users:", all_users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
