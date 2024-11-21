# flask_blog/init_db.py
import sqlite3

# Open a connection to create or connect to the database
connection = sqlite3.connect('database.db')

# Open the schema.sql file and execute its contents
with open('schema.sql') as f:
    connection.executescript(f.read())

# Create a cursor to execute SQL commands
cur = connection.cursor()

# Insert initial data into the posts table with the correct number of values
cur.execute("INSERT INTO posts (title, content, result) VALUES (?, ?, ?)",
            ('First Post', 'Content for the first post', 'Win'))

cur.execute("INSERT INTO posts (title, content, result) VALUES (?, ?, ?)",
            ('Second Post', 'Content for the second post', 'Win'))

# Commit the changes and close the connection
connection.commit()
connection.close()
