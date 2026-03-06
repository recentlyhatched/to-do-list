import sqlite3

conn = sqlite3.connect("todolist.db")
print("Connected to database")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
               id INTERGER PRIMARY KEY,
               name TEXT NOT NULL,
               is_complete BOOLEAN NOT NULL DEFAULT 0)
               """)

cursor.execute("INSERT INTO tasks (name, is_complete) VALUES (?, ?)", ("Clean bathroom", True))

conn.commit()
conn.close()