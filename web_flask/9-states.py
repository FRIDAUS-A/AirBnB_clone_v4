#!/usr/bin/python3
"""
This script starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """removes the current SQLAlchemy session"""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<state_id>", strict_slashes=False)
def cities_by_states(state_id=None):
    """renders cities by states"""
    if not state_id:
        states = storage.all(State).values()
        return render_template("9-states.html", states=states)
    else:
        state = storage.get(State, state_id)
        return render_template("9-states.html", state=state)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
