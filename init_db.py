import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['majikyouser'],
        password=os.environ['tis_the_season'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS files;')
cur.execute('CREATE TABLE files (id serial PRIMARY KEY,'
                                 'file_name TEXT NOT NULL,'
                                 'file_blob BLOB NOT NULL'
                                 )

# Insert data into the table
with open("./files/README_(Do_not_delete_please).txt", "rb") as file:
    cur.execute("INSERT INTO files (file_name, file_blob) VALUES (%s, %s)",
              ("README_(Do_not_delete_please).txt", file.read())
              )

conn.commit()

cur.close()
conn.close()