from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "database.db"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def get_task():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()
    return rows


def add_task(task):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()

    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")

        #makes sure task is not empty
        if task and task.strip():
            add_task(task)
        
        return redirect("/")

    tasks = get_task()
    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>") # convert to integer
def delete(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # toggle the completed status
    cursor.execute("""
        UPDATE tasks
        SET completed = CASE WHEN completed=0 THEN 1 ELSE 0 END
        WHERE id=?
    """, (id,))
    
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)