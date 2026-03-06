ChromeOS (Debian-based Linux) protects the system Python from direct pip installs. You must install packages in a virtual environment.
`python3 -m venv venv` <br>
`source venv/bin/activate`

Install flask
`pip install flask`

Run server
`python3 app.py`

Close server
`deactivate`