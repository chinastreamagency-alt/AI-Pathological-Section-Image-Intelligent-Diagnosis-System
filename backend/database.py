import aiosqlite
from config import DATABASE_URL

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_name TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    image_width INTEGER,
    image_height INTEGER,
    question TEXT NOT NULL DEFAULT '',
    image_description TEXT DEFAULT '',
    diagnosis_result TEXT DEFAULT '',
    model_used TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


async def get_db():
    db = await aiosqlite.connect(DATABASE_URL)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    db = await get_db()
    await db.execute(CREATE_TABLE_SQL)
    await db.commit()
    await db.close()
