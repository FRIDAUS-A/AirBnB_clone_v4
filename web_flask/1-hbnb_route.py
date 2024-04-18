#!/usr/bin/python3
"""
Write a script that starts a Flask web application
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return f"Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return f"HBNB"


if __name__ == '__main__':
    app.run()
