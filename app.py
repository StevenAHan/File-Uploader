from re import I
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, make_response

app = Flask(__name__)

app.config["SECRET_KEY"] = "HAVEFUN!"

# To insert a file into the database
def insert_into_database(file):
    connection = sqlite3.connect("database.db")


    cur = connection.cursor()

    file_name = file.filename.replace(" ", "_")

    cur.execute("INSERT INTO files (file_name, file_blob) VALUES (?, ?)",
              (file_name, file.read())
              )

    connection.commit()
    connection.close()

# To get a file from the database
def get_from_database(file_name):
    connection = sqlite3.connect("database.db")

    cur = connection.cursor()

    cur.execute("SELECT file_blob FROM files WHERE file_name=?", (file_name,))

    file_blob = cur.fetchall()[0][0]

    connection.commit()
    connection.close()
    
    return file_blob

# To remove a file from the database
def remove_from_database(file_name):
    connection = sqlite3.connect("database.db")

    cur = connection.cursor()

    cur.execute("DELETE FROM files WHERE file_name=?", (file_name,))

    connection.commit()
    connection.close()

# Default route
@app.route("/")
def index():
    conn = get_db_connection()
    files = conn.execute("SELECT * FROM files").fetchall()
    conn.close()
    return render_template("index.html", files=files)

# Route to Upload a file onto the database
@app.route("/", methods=["GET", "POST", "DELETE"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if(file.filename != ""):
            insert_into_database(file)
        
    return redirect(url_for("index"))

# Route to Download a file from the database
@app.route("/download/<file_name>")
def download_file(file_name):
    f_blob =get_from_database(file_name)
    image_binary = f_blob
    response = make_response(image_binary)
    response.headers.set(
        'Content-Disposition', 'attachment', filename=file_name)
    return response

# Route to Delete a file from the database
@app.route("/delete/<file_name>")
def delete_file(file_name):
    remove_from_database(file_name)
    return redirect(url_for("index"))

# Connects to Database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
    
if __name__ == "__main__":
    app.run(debug=True)