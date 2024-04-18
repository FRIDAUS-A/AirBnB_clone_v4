#!/usr/bin/python3
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import request, jsonify, redirect
import json

@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],  strict_slashes=False)
def amenity(amenity_id=None):
    if request.method == "GET":
        if not amenity_id:
            listAmenity = []
            amenities = storage.all(Amenity)
            for amenity in amenities.values():
                listAmenity.append(amenity.to_dict())
            return jsonify(listAmenity)
        else:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                return jsonify(amenity.to_dict())
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "DELETE":
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return jsonify({})
        else:
            return jsonify({"error": "Not found"})
    if request.method == "POST":
        if not amenity_id:
            try:
                data = request.get_json()
            except:
                response = jsonify({'error': 'Not a JSON'})
                response.status_code = 400
                return response
            if "name" not in data:
                response = jsonify({'error': 'Missing name'})
                response.status_code = 400
                return response
            amenity = Amenity(**data)
            storage.new(amenity)
            storage.save()
            response = jsonify(amenity.to_dict())
            response.status_code = 201
            return response
    if request.method == "PUT":
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)
            if not amenity:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            else:
                try:
                    data = request.get_json()
                except:
                    response = jsonify({'error': 'Not a JSON'})
                    response.status_code = 400
                    return response
                amenity = storage.get(Amenity, amenity_id)
                amenityDict = amenity.to_dict()
                for key, value in data.items():
                    amenityDict[key] = value
                amenity.delete()
                storage.save()
                amenity = Amenity(**amenityDict)
                amenity.save()
                response = jsonify(amenity.to_dict())
                response.status_code = 200
                return response
