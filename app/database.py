import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect('catalog.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS catalog("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT,"
                "desc TEXT, "
                "price TEXT, "
                "video TEXT, "
                "type TEXT)")
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()


async def add_item(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO catalog (name, desc, price, video, type) VALUES (?, ?, ?, ?, ?)",
                    (data['name'], data['desc'], data['price'], data['video'], data['type']))
        db.commit()

async def get_items_by_type(item_type):
    cur.execute("SELECT * FROM catalog WHERE type = ?", (item_type,))
    items = cur.fetchall()
    return items