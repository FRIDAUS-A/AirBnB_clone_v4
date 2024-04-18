#!/usr/bin/python3
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import request, jsonify, redirect
import json

@app_views.route("/places/<place_id>", methods=["GET", "POST", "DELETE", "PUT"])
@app_views.route("/cities/<city_id>/places", methods=["GET", "POST", "DELETE", "PUT"])
def place(place_id=None, city_id=None):
    if request.method == "GET":
        print("GET")
        if city_id:
            city = storage.get(City, city_id)
            if city:
                allPlace = []
                places = city.places
                for place in places:
                    allPlace.append(place.to_dict())
                return jsonify(allPlace)
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                return jsonify(place.to_dict())
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "DELETE":
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                place.delete()
                storage.save()
                return jsonify({})
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "POST":
        if city_id:
            city = storage.get(City, city_id)
            if not city:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            try:
                data = request.get_json()
            except:
                response = jsonify({"error": "Not json"}) 
                response.status_code = 400
                return response
            if "user_id" not in data:
                response = jsonify({"error": "Missing user_id"})
                response.status_code = 400
                return response
            place = Place(**data, city_id=city_id)
            user_id = place.user_id
            user = storage.get(User, user_id)
            if not user:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            if "name" not in data:
                response = jsonify({"error": "Missing name"})
                response.status_code = 400
                return response
            storage.new(place)
            storage.save()
            place = storage.get(Place, place.id)
            response = jsonify(place.to_dict())
            response.status_code = 201
            return response
    if request.method == "PUT":
        if place_id:
            print("here")
            place = storage.get(Place, place_id)
            if not place:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            try:
                data = request.get_json()
            except:
                response = jsonify({"error": "Not json"})
                response.status_code = 400
                return response
            placeDict = place.to_dict()
            place.delete()
            storage.save()
            for key, value in data.items():
                placeDict[key] = value
            place = Place(**placeDict)
            place.save()
            place = storage.get(Place, place_id)
            return jsonify(place.to_dict())
