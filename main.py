from re import I
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = "HAVEFUN!"

# To insert a file into the database
def insert_into_database(file):
    connection = sqlite3.connect("database.db")


    cur = connection.cursor()

    cur.execute("INSERT INTO files (file_name, file_blob) VALUES (?, ?)",
              (file.filename, file.read())
              )

    connection.commit()
    connection.close()


def get_from_database(file_name):
    connection = sqlite3.connect("database.db")

    cur = connection.cursor()

    cur.execute("SELECT file_blob FROM files WHERE file_name=?", (file_name,))

    file = cur.fetchall()[0][0]

    connection.commit()
    connection.close()
    
    return file

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
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        insert_into_database(file)
        leFile = get_from_database("download.html")

        
    return redirect(url_for("index"))
    
# Connects to Database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
    
if __name__ == "__main__":
    app.run(debug=True)