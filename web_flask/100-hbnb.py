#!/usr/bin/python3

from flask import Flask, render_template
app = Flask(__name__)
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User

@app.teardown_appcontext
def tear_down(self):
    """remove the current session"""
    storage.close()

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """the full page"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    places_and_names = {}
    for place in places:
        user = storage.get(User, place.user_id)
        full_name = user.first_name + ' ' + user.last_name
        places_and_names[full_name] = place
    return render_template('100-hbnb.html', states=states, amenities=amenities, places_and_names=places_and_names,
    places=places)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
