import sqlite3
from init_db import insert_into_database, write_to_file, convert_into_binary
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

app.config['SECRET_KEY'] = "HAVEFUN!"

@app.route('/')
def index():
    conn = get_db_connection()
    files = conn.execute('SELECT * FROM files').fetchall()
    conn.close()    
    return render_template('index.html', files=files)

@app.route('/', methods=('GET', 'POST'))
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        insert_into_database(file.name, convert_into_binary(file))
    else:
        flash("You must insert a file...")

    return redirect(url_for('index'))

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
if __name__ == "__main__":
    app.run(debug=True)