#!/usr/bin/python3
"""
Write a script that starts a Flask web application
"""
from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return f"Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return f"HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    text = text.split('_')
    text = ' '.join(text)
    return f"C {escape(text)}"


if __name__ == '__main__':
    app.run()
