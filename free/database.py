import aiosqlite
from datetime import datetime
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                code TEXT,
                url TEXT UNIQUE,
                date_collecte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT
            )
        ''')
        await db.commit()

async def add_item(item):
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute('''
                INSERT INTO items (title, type, code, url, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (item['title'], item['type'], item.get('code'), item['url'], item['source']))
            await db.commit()
        except aiosqlite.IntegrityError:
            pass  # Doublon ignoré

async def get_today_items():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('''
            SELECT * FROM items 
            WHERE DATE(date_collecte) = DATE('now', 'localtime')
        ''')
        return await cursor.fetchall()

async def clear_today():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            DELETE FROM items 
            WHERE DATE(date_collecte) = DATE('now', 'localtime')
        ''')
        await db.commit()
async def add_subscriber(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                user_id INTEGER PRIMARY KEY
            )
        ''')
        await db.execute('INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)', (user_id,))
        await db.commit()

async def get_subscribers():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                user_id INTEGER PRIMARY KEY
            )
        ''')
        cursor = await db.execute('SELECT user_id FROM subscribers')
        return [row[0] for row in await cursor.fetchall()]