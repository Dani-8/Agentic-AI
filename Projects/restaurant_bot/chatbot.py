import sqlite3
import json

def connect_db():
    return sqlite3.connect('restaurant.db')

def get_menu_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu')
    menu = cursor.fetchall()
    conn.close()
    return menu

def get_menu_description(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT item, price, cat FROM menu WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def place_order(item_id, user_detail):
    conn = connect_db()
    cursor = conn.cursor()
    item = get_menu_description(item_id)
    if not item:
        return None
    total = item[1]  # price
    order_status = 'confirmed'
    user_json = json.dumps(user_detail)
    cursor.execute('INSERT INTO orders (itemid, orderstatus, totalamount, userdetail) VALUES (?, ?, ?, ?)',
                   (item_id, order_status, total, user_json))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def cancel_order(order_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET orderstatus = "canceled" WHERE orderid = ?', (order_id,))
    conn.commit()
    conn.close()

def track_order(order_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE orderid = ?', (order_id,))
    order = cursor.fetchone()
    conn.close()
    return order

def chatbot():
    print("Welcome to Grok Eats! How can I help? (Type 'exit' to quit)")
    
    while True:
        user_input = input("You: ").lower()
        if 'exit' in user_input:
            print("Goodbye!")
            break
        elif 'menu' in user_input:
            # Menu listing/description (RAG-like retrieval)
            menu = get_menu_list()
            print("Menu:")
            for item in menu:
                print(f"ID: {item[0]}, Item: {item[1]}, Price: ${item[2]}, Category: {item[3]}")
        elif 'describe' in user_input or 'detail' in user_input:
            # Assume user provides ID; extend with parsing for real
            try:
                item_id = int(user_input.split()[-1])
                item = get_menu_description(item_id)
                if item:
                    print(f"Item: {item[0]}, Price: ${item[1]}, Category: {item[2]}")
                else:
                    print("Item not found.")
            except:
                print("Please provide item ID.")
        elif 'order' in user_input:
            # Order taking
            try:
                item_id = int(user_input.split()[-1])
                name = input("Your name: ")
                email = input("Your email: ")
                user_detail = {"name": name, "email": email}
                order_id = place_order(item_id, user_detail)
                if order_id:
                    print(f"Order confirmed! Order ID: {order_id}, Total: ${get_menu_description(item_id)[1]}")
                else:
                    print("Invalid item.")
            except:
                print("Please provide item ID.")
        elif 'cancel' in user_input:
            try:
                order_id = int(user_input.split()[-1])
                cancel_order(order_id)
                print(f"Order {order_id} canceled.")
            except:
                print("Please provide order ID.")
        elif 'track' in user_input or 'status' in user_input:
            try:
                order_id = int(user_input.split()[-1])
                order = track_order(order_id)
                if order:
                    print(f"Order ID: {order[0]}, Status: {order[2]}, Total: ${order[3]}, User: {order[4]}")
                else:
                    print("Order not found.")
            except:
                print("Please provide order ID.")
        else:
            # Customer rep fallback
            print("Sorry, I didn't understand. Contact support at support@grokeats.com.")

if __name__ == '__main__':
    chatbot()
