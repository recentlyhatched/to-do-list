ChromeOS (Debian-based Linux) protects the system Python from direct pip installs. You must install packages in a virtual environment.
`python3 -m venv venv` <br>
`source venv/bin/activate`

Install flask
`pip install flask`

Run server
`python3 app.py`

Close server
ctrl + C

Exit virtual environment
`deactivate`

Notes
I used `"INSERT INTO tasks (task) VALUES (?)", (task,)` to prevent SQL injection to build a secure app

I used `task = request.form.get("task")` instead of `task = request.form["task"]` to handle empty submissions