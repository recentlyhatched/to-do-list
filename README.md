Run unpdates and check if you have sqlite3 installed
`sudo apt update`
`sqlite3 --version`

If sqlite3 is not installed, run this command in the terminal:
`sudo apt install sqlite3`

ChromeOS (Debian-based Linux) protects the system Python from direct pip installs. You must install packages in a virtual environment.
`python3 -m venv venv`
`source venv/bin/activate`

Install flask
`pip install flask`

Run server
`python3 app.py`

Close server
`deactivate`