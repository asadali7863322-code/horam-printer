import json
from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Session Secret Key
app.secret_key = "horam_printer_secret"

# Upload Folder Configuration
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ==========================================
# DATABASE HELPER FUNCTIONS
# ==========================================

def get_db_connection():
    conn = sqlite3.connect("horam.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings LIMIT 1")
    settings = cursor.fetchone()
    conn.close()
    return settings

def create_settings_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website_name TEXT DEFAULT 'HORAM PRINTER',
        logo TEXT DEFAULT '',
        theme TEXT DEFAULT 'luxury',
        whatsapp TEXT DEFAULT '',
        email TEXT DEFAULT '',
        address TEXT DEFAULT ''
    )
    """)

    cursor.execute("SELECT * FROM settings")
    if cursor.fetchone() is None:
        cursor.execute("""
        INSERT INTO settings (website_name, logo, theme, whatsapp, email, address)
        VALUES ('HORAM PRINTER', '', 'luxury', '', '', '')
        """)

    conn.commit()
    conn.close()

def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Admin Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Gallery Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gallery(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        image TEXT
    )
    """)

    # Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        phone TEXT,
        product TEXT,
        quantity TEXT,
        message TEXT,
        status TEXT DEFAULT 'Pending',
        order_date TEXT
    )
    """)

    # Default Admin Create
    cursor.execute("SELECT * FROM admin")
    admin = cursor.fetchone()

    if not admin:
        cursor.execute("""
        INSERT INTO admin(username, password)
        VALUES(?, ?)
        """, ("admin", "1234"))

    conn.commit()
    conn.close()


# Initialize Database Tables
create_database()
create_settings_table()


# ==========================================
# ROUTES
# ==========================================

# 1. HOME PAGE
@app.route("/")
def home():
    settings = get_settings()
    settings_dict = dict(settings) if settings else {
        "website_name": "HORAM PRINTER",
        "theme": "luxury",
        "logo": "",
        "whatsapp": "",
        "email": "",
        "address": ""
    }
    return render_template("index.html", settings=settings_dict)


# 2. ADMIN LOGIN
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM admin
            WHERE username=? AND password=?
        """, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["admin"] = username
            return redirect("/dashboard")
        else:
            return "Wrong Username or Password"

    return render_template("admin_login.html")


# 3. ADMIN DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gallery")
    images = cursor.fetchall()

    search = request.args.get("search", "")
    if search:
        cursor.execute("""
            SELECT * FROM orders
            WHERE customer_name LIKE ?
            ORDER BY id DESC
        """, ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM orders ORDER BY id DESC")

    orders = cursor.fetchall()
    conn.close()

    total_gallery = len(images)
    total_orders = len(orders)
    pending_orders = sum(1 for order in orders if order['status'] == "Pending")
    completed_orders = sum(1 for order in orders if order['status'] == "Completed")

    return render_template(
        "admin_dashboard.html",
        images=images,
        orders=orders,
        settings=get_settings(),
        total_gallery=total_gallery,
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        search=search
    )


# 4. GALLERY IMAGE UPLOAD
@app.route("/upload", methods=["POST"])
def upload():
    if "admin" not in session:
        return redirect("/admin")

    title = request.form["title"]
    image = request.files["image"]

    if image:
        filename = image.filename
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO gallery(title, image)
            VALUES(?, ?)
        """, (title, filename))
        conn.commit()
        conn.close()

    return redirect("/dashboard")


# 5. PLACE ORDER
from datetime import datetime

@app.route("/order", methods=["GET", "POST"])
def order():
    settings = get_settings()

    if request.method == "POST":
        customer_name = request.form["customer_name"]
        phone = request.form["phone"]
        product = request.form["product"]
        quantity = request.form["quantity"]
        message = request.form["message"]
        order_date = datetime.now().strftime("%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_name, phone, product, quantity, message, order_date)
            VALUES(?, ?, ?, ?, ?, ?)
        """, (customer_name, phone, product, quantity, message, order_date))
        conn.commit()
        conn.close()

        return render_template("order.html", settings=settings, success=True)

    return render_template("order.html", settings=settings)


# 6. GALLERY PAGE
@app.route("/gallery")
def gallery():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gallery")
    images = cursor.fetchall()
    conn.close()

    return render_template("gallery.html", images=images, settings=get_settings())


# 7. DELETE GALLERY POST
@app.route("/delete/<int:id>")
def delete_post(id):
    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gallery WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# 8. SAVE WEBSITE SETTINGS
@app.route("/save-settings", methods=["POST"])
def save_settings():
    if "admin" not in session:
        return redirect("/admin")

    website_name = request.form.get("website_name")
    whatsapp = request.form.get("whatsapp")
    email = request.form.get("email")
    address = request.form.get("address")
    theme = request.form.get("theme")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE settings
        SET website_name=?, whatsapp=?, email=?, address=?, theme=?
        WHERE id=1
    """, (website_name, whatsapp, email, address, theme))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# 9. UPLOAD WEBSITE LOGO
@app.route("/upload-logo", methods=["POST"])
def upload_logo():
    if "admin" not in session:
        return redirect("/admin")

    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE settings SET logo = ? WHERE id = 1", (filename,))
            except:
                cursor.execute("ALTER TABLE settings ADD COLUMN logo TEXT")
                cursor.execute("UPDATE settings SET logo = ? WHERE id = 1", (filename,))

            conn.commit()
            conn.close()
            print("Logo successfully saved:", filename)

    return redirect("/dashboard")


# 10. UPDATE ORDER STATUS
@app.route("/order-status/<int:id>/<status>")
def order_status(id, status):
    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# 11. DELETE ORDER
@app.route("/delete-order/<int:id>")
def delete_order(id):
    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# 12. SHOW UPLOADED FILES / LOGO
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ==========================================
# START SERVER
# ==========================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )