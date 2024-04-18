#!/usr/bin/python3
"""
Write a script that starts a Flask web application
"""
from flask import Flask
from markupsafe import escape
from flask import render_template
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


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/")
def python_route(text="is cool"):
    text = text.split('_')
    text = " ".join(text)
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n: int):
    if isinstance(n, int):
        return f"{escape(n)} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n: int):
    if isinstance(n, int):
        return render_template("5-number.html", n=n)


if __name__ == '__main__':
    app.run()
