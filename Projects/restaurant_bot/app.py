from flask import Flask, request, jsonify, render_template, session
import sqlite3, json

app = Flask(__name__)
app.secret_key = "grokeats"

def db_query(query, params=()):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

@app.route("/")
def home():
    session.clear()  # fresh start every reload
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["msg"].lower().strip()

    # Step 1: Get name & email
    if not session.get("user"):
        if "my name is" in msg or "i am" in msg:
            name = msg.split("is")[-1].strip().title()
            session["user"] = {"name": name}
            return jsonify({"reply": f"Hi {name}! What's your email?"})
        if "@" in msg and "." in msg:
            session["user"]["email"] = msg
            return jsonify({"reply": f"Thanks {session['user']['name']}! Type **menu** to see items"})
        return jsonify({"reply": "Hi! Tell me your name first (e.g. My name is Alex)"})

    user = session["user"]
    name = user["name"]

    # Normal commands
    if "menu" in msg:
        items = db_query("SELECT id,item,price,cat FROM menu")
        resp = "<b>Menu:</b><br>" + "<br>".join([f"{i[0]}. {i[1]} – ${i[2]} ({i[3]})" for i in items])
        return jsonify({"reply": resp})

    if msg.startswith("order"):
        try:
            item_id = int(msg.split()[-1])
            item = db_query("SELECT item,price FROM menu WHERE id=?", (item_id,))[0]
            user_json = json.dumps(user)
            db_query("INSERT INTO orders (itemid, orderstatus, totalamount, userdetail) VALUES (?,?,?,?)",
                     (item_id, "confirmed", item[1], user_json))
            resp = f"Order placed!<br>{item[0]} – ${item[1]}<br>Order saved in dashboard"
        except:
            resp = "Type: **order 1** or **order 2** etc."
        return jsonify({"reply": resp})

    if msg.startswith("cancel") or "cancel" in msg:
        try:
            order_id = int(msg.split()[-1])
            db_query("UPDATE orders SET orderstatus='canceled' WHERE orderid=?", (order_id,))
            resp = f"Order {order_id} canceled"
        except:
            resp = "Type: **cancel 1** (use your order number from dashboard)"
        return jsonify({"reply": resp})

    return jsonify({"reply": "Type: **menu** | **order 2** | **cancel 1**"})

if __name__ == "__main__":
    app.run(debug=True) 