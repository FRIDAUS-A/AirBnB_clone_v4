#!/usr/bin/python3
"""Starts a Flask Web app"""
from flask import Flask, jsonify
from models import storage
import os
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the database again at the end of the request."""
    storage.close()

@app.errorhandler(404)
def handle_exception(e):
    response = jsonify({"message": "Not found"})
    response.status_code = 404
    return response

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
