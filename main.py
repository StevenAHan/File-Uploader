import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = "HAVEFUN!"

# To insert a file into the database
def insert_into_database(file_name, file):
    connection = sqlite3.connect("database.db")

    with open("schema.sql") as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO files (file_name, file_blob) VALUES (?, ?)",
              (file_name, file.read())
              )

    connection.commit()
    connection.close()

# To get a file from the database
def get_file(file_name):
    return ...

# default route
@app.route("/")
def index():
    conn = get_db_connection()
    files = conn.execute("SELECT * FROM files").fetchall()
    conn.close()    
    return render_template("index.html", files=files)

# To Upload a file onto the database
@app.route("/", methods=("GET", "POST"))
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        insert_into_database(file.filename, file)
    
    
    if request.method == "GET":
        file = ...

    return redirect(url_for("index"))

# Connects to Database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
    
if __name__ == "__main__":
    app.run(debug=True)