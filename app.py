from re import I
from flask import Flask, render_template, request, url_for, flash, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://msizwihjuryyem:160b6d8fb521e2255d6f08aef4500e4028758af1a927cf5a046155ac663779b4@ec2-3-219-19-205.compute-1.amazonaws.com:5432/dbgggdr11demc6"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class files(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    file_name = db.Column(db.String(100))
    file_blob = db.Column(db.String(65535))
    def __init__(self, file_name, file_blob):
        self.file_name = file_name
        self.file_blob = file_blob

with app.app_context():
    db.create_all()

# To insert a file into the database
def insert_into_database(file):
    db.session.add(file)
    db.session.commit()

# To get a file from the database
def get_from_database(file_name):
    file = files.query.filter_by(file_name = file_name).first()
    return file.file_blob

# To remove a file from the database
def remove_from_database(file_name):
    file = files.query.filter_by(file_name = file_name).first()
    db.session.delete(file)
    db.session.commit()

# Default route
@app.route("/")
def index():
    the_files = files.query.all()
    return render_template("index.html", files=the_files)

# Route to Upload a file onto the database
@app.route("/", methods=["GET", "POST", "DELETE"])
def upload_file():
    if request.method == "POST":
        the_file = request.files["file"]
        file = files(file_name = the_file.filename.replace(" ", "_"), file_blob = the_file.read())
        if(file.file_name != ""):
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
    
if __name__ == "__main__":
    app.run(debug=True)