import sqlite3

def init_db():
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            description TEXT,
            stock INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            phone_number TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, description, stock FROM products WHERE stock > 0")
    rows = cur.fetchall()
    conn.close()
    return rows

def buy_product(user_id, product_id):
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()
    cur.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
    product = cur.fetchone()
    if not product:
        conn.close()
        return None
    # Здесь можно зарезервировать реальный номер из другой таблицы
    # Упрощённо: выдаём фейковый номер
    fake_number = f"+7999123{1000 + user_id % 10000}"
    cur.execute("INSERT INTO purchases (user_id, product_id, phone_number, status) VALUES (?, ?, ?, 'paid')",
                (user_id, product_id, fake_number))
    conn.commit()
    conn.close()
    return fake_number
