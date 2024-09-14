import os
import aiosqlite


DATABASE_PATH = os.getenv("DATABASE_PATH", "/data/mydatabase.db")


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


async def save_data_to_sqlite(
    email: str, phone: str, management_company: str, address: str
):
    """Save or update user data in the SQLite database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (email, phone, management_company, address)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET 
                phone = excluded.phone,
                management_company = excluded.management_company,
                address = excluded.address
            """,
            (email, phone, management_company, address),
        )
        await db.commit()


async def create_sqlite_table():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                phone TEXT,
                management_company TEXT,
                address TEXT
            )
            """
        )
        await db.commit()


async def get_data_from_sqlite(email: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT email, phone, management_company, address FROM users WHERE email = ?",
            (email,),
        ) as cursor:
            row = await cursor.fetchone()
            return row
