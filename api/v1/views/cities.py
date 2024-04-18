#!/usr/bin/python3
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import request, jsonify, redirect
import json

@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
@app_views.route("/states/<state_id>/cities", methods=["GET", "POST", "DELETE"])
def city(state_id=None, city_id=None):
    if request.method == "GET":
        if state_id:
            state = storage.get(State, state_id)
            if state:
                allCity = []
                cities = state.cities
                for city in cities:
                    allCity.append(city.to_dict())
                return jsonify(allCity)
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
        if city_id:
            city = storage.get(City, city_id)
            if city:
                return jsonify(city.to_dict())
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "DELETE":
        if city_id:
            city = storage.get(City, city_id)
            if city:
                city.delete()
                storage.save()
                return jsonify({})
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "POST":
        if state_id:
            state = storage.get(State, state_id)
            if state:
                pass
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            try:
                data = request.get_json()
            except:
                response = jsonify({"error": "Not a JSON"})
                response.status_code = 400
                return response
            if "name" not in data:
                response = jsonify({"error": "Missing name"})
                response.status_code = 400
            city = City(**data, state_id=state.id)
            storage.new(city)
            storage.save()
            city = storage.get(City, city.id)
            response = jsonify(city.to_dict())
            response.status_code = 201
            return response
    if request.method == "PUT":
        if city_id:
            city = storage.get(City, city_id)
            if city:
                pass
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            try:
                data = request.get_json()
            except:
                response = jsonify({"error": "Not a JSON"})
                response.status_code = 401
                return response
            if "name" not in data:
                response = jsonify({"error": "Missing name"})
                response.status_code = 400
                return response
            cityDict = city.to_dict()
            city.delete()
            storage.save()
            for key, value in data.items():
                cityDict[key] = value
            city = City(**cityDict)
            city.save()
            city = storage.get(City, city_id)
            return jsonify(city.to_dict())
