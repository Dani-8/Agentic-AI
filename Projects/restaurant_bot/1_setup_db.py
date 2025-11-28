import sqlite3

def setup_database():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Create menu table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            cat TEXT NOT NULL
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            orderid INTEGER PRIMARY KEY AUTOINCREMENT,
            itemid INTEGER NOT NULL,
            orderstatus TEXT NOT NULL,  -- e.g., 'pending', 'confirmed', 'canceled'
            totalamount REAL NOT NULL,
            userdetail TEXT NOT NULL  -- e.g., JSON string: {"name": "John", "email": "john@example.com"}
        )
    ''')
    
    # Insert sample menu data (RES-KB)
    sample_menu = [
        ('Burger', 10.99, 'Main'),
        ('Pizza', 12.99, 'Main'),
        ('Salad', 8.99, 'Appetizer'),
        ('Soda', 2.99, 'Drink')
    ]
    cursor.executemany('INSERT INTO menu (item, price, cat) VALUES (?, ?, ?)', sample_menu)
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()