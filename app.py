import json
from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3
import os

# ===========================
# Get Website Settings
# ===========================

def get_settings():

    conn = sqlite3.connect("horam.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM settings LIMIT 1")

    settings = cursor.fetchone()

    conn.close()

    return settings

def create_settings_table():
    conn = sqlite3.connect("horam.db")
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
        INSERT INTO settings
        (website_name,logo,theme,whatsapp,email,address)

        VALUES

        ('HORAM PRINTER','','luxury','','','')
        """)

    conn.commit()
    conn.close()

app = Flask(__name__)

# Session Secret Key
app.secret_key = "horam_printer_secret"


# Upload Folder
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# =========================
# DATABASE CREATE
# =========================

def create_database():

    conn = sqlite3.connect("horam.db")

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



    # Default Admin Create

    cursor.execute(
        "SELECT * FROM admin"
    )


    admin = cursor.fetchone()


    if not admin:

        cursor.execute(
            """
            INSERT INTO admin(username,password)
            VALUES(?,?)
            """,
            ("admin","1234")
        )



    conn.commit()

    conn.close()



create_database()



# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    settings = get_settings()

    print(dict(settings))

    return render_template(
        "index.html",
        settings=settings
    )




# =========================
# ADMIN LOGIN
# =========================


@app.route("/admin", methods=["GET","POST"])
def admin_login():


    if request.method == "POST":


        username = request.form["username"]

        password = request.form["password"]



        conn = sqlite3.connect("horam.db")

        cursor = conn.cursor()



        cursor.execute(
            """
            SELECT * FROM admin
            WHERE username=? AND password=?
            """,
            (username,password)
        )


        user = cursor.fetchone()


        conn.close()



        if user:

            session["admin"] = username

            return redirect("/dashboard")


        else:

            return "Wrong Username or Password"



    return render_template("admin_login.html")





# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/admin")


    conn = sqlite3.connect("horam.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gallery")

    images = cursor.fetchall()

    conn.close()


    return render_template(
        "admin_dashboard.html",
        images=images
    )



# =========================
# RUN APP
# =========================

# =========================
# IMAGE UPLOAD
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    if "admin" not in session:
        return redirect("/admin")


    title = request.form["title"]

    image = request.files["image"]


    if image:

        filename = image.filename


        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )


        conn = sqlite3.connect("horam.db")

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO gallery(title,image)
            VALUES(?,?)
            """,
            (title,filename)
        )


        conn.commit()

        conn.close()


    return redirect("/dashboard")

# =========================
# GALLERY PAGE
# =========================

@app.route("/gallery")
def gallery():

    conn = sqlite3.connect("horam.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM gallery"
    )

    images = cursor.fetchall()

    conn.close()


    settings = get_settings()


    return render_template(
        "gallery.html",
        images=images,
        settings=settings
    )

# =========================
# DELETE GALLERY POST
# =========================

@app.route("/delete/<int:id>")
def delete_post(id):

    if "admin" not in session:
        return redirect("/admin")


    conn = sqlite3.connect("horam.db")

    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM gallery WHERE id=?",
        (id,)
    )


    conn.commit()

    conn.close()


    return redirect("/dashboard")

# ===========================
# Save Website Settings
# ===========================

@app.route("/save-settings", methods=["POST"])
def save_settings():

    website_name = request.form.get("website_name")
    whatsapp = request.form.get("whatsapp")
    email = request.form.get("email")
    address = request.form.get("address")
    theme = request.form.get("theme")
    print("Selected Theme:", theme)

    conn = sqlite3.connect("horam.db")
    cursor = conn.cursor()

    cursor.execute("""
UPDATE settings
SET website_name=?,
    whatsapp=?,
    email=?,
    address=?,
    theme=?
WHERE id=1
""",
(
    website_name,
    whatsapp,
    email,
    address,
    theme
))

    conn.commit()
    conn.close()

    return redirect("/dashboard")



# ===========================
# Upload Website Logo
# ===========================

@app.route("/upload-logo", methods=["POST"])
def upload_logo():

    # ... آپ کا موجودہ کوڈ ...

    return redirect("/dashboard")


# ===========================
# SHOW UPLOADED FILES
# ===========================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )



if __name__ == "__main__":

    create_database()
    create_settings_table()

    app.run(debug=True)