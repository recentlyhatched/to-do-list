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
        completed INTEGER DEFAULT 0,
        deadline TEXT,
        priority TEXT
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


def add_task(task, deadline, priority):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (task, deadline, priority) VALUES (?, ?, ?)", (task, deadline, priority))
    conn.commit()

    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    if request.method == "POST":
        task = request.form.get("task")
        deadline = request.form.get("deadline")
        priority = request.form.get("priority")

        #makes sure task is not empty
        if task and task.strip():
            add_task(task, deadline, priority)
        
        return redirect("/")

    # filtering
    priority_filter = request.args.get("priority")

    if priority_filter:
        cursor.execute("SELECT * FROM tasks WHERE priority=?", (priority_filter,))
    else:
        cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()
    conn.close

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


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    if request.method == "POST":
        # get task, deadline and priority inputs
        new_task = request.form.get("task")
        new_deadline = request.form.get("deadline")
        new_priority = request.form.get("priority")

        if new_task and new_task.strip():
            cursor.execute("""
                           UPDATE tasks
                           SET task=?, deadline=?, priority=?
                           WHERE id=?
                           """, (new_task, new_deadline, new_priority, id))
            conn.commit()
        conn.close()
        return redirect("/")
    
    # GET request - show current task in a form
    cursor.execute("SELECT task, deadline, priority FROM tasks WHERE id=?", (id,))
    task = cursor.fetchone()
    conn.close()
    if task:
        return render_template(
            "edit.html",
            task_id=id,
            task_text=task[0],
            deadline=task[1],
            priority=task[2]
            )
    else:
        return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)