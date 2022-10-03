import os
import sqlite3
from sqlite3 import Error

def main():
  connection = sqlite3.connect("database.db")

  with open("schema.sql") as f:
      connection.executescript(f.read())

  cur = connection.cursor()

  with open("./files/README_(Do_not_delete_please).txt", "rb") as file:
    cur.execute("INSERT INTO files (file_name, file_blob) VALUES (?, ?)",
              ("README_(Do_not_delete_please).txt", file.read())
              )

  connection.commit()
  connection.close()

if __name__ == "__main__":
  main()