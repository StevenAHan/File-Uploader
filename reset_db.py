import os
import sqlite3
from sqlite3 import Error

def main():
  connection = sqlite3.connect("database.db")

  with open("schema.sql") as f:
      connection.executescript(f.read())

  cur = connection.cursor()
  connection.commit()
  connection.close()

if __name__ == "__main__":
  main()