#!/usr/bin/python3
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models import storage
from flask import request, jsonify, redirect
import json

@app_views.route("/reviews/<review_id>", methods=["GET", "POST", "DELETE", "PUT"])
@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST", "DELETE"])
def review(review_id=None, place_id=None):
    if request.method == "GET":
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                allReview = []
                reviews = place.reviews
                for review in reviews.values():
                    allReview.append(reviews.to_dict())
                return jsonify(allReview)
            else:
                respoonse = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
        if review_id:
            review = storage.get(Review, review_id)
            if review:
                return jsonify(review.to_dict())
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "DELETE":
        if review_id:
            review = storage.get(Review, review_id)
            if review:
                review.delete()
                storage.save()
                return jsonify({})
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "POST":
        if place_id:
            place = storage.get(Place, place_id)
            if not place:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            try:
                data = request.get_json()
            except:
                response = jsonify({"error": "Not a JSON"})
                response.status_code = 400
                return response
            if "user_id" not in data:
                response = jsonify({"error": "Missing user_id"})
                response.status_code = 400
                return response
            user_id = storage.get(User, place.user_id)
            if not user_id:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            if "text" not in data:
                response = jsonify({"error": "Missing text"})
                response.status_code = 400
                return response
            review = Review(**data, place_id=place_id)
            storage.new(review)
            storage.save()
            review = storage.get(Review, review.id)
            response = jsonify(review.to_dict())
            response.status_code = 201
            return response
    if request.method == "PUT":
        print("here")
        if review_id:
            review = storage.get(Review, review_id)
            if not review:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
            try:
                data = request.get_json()
            except:
                response = jsonify({"error": "Not a JSON"})
                response.status_code = 400
                return response
            reviewDict = review.to_dict()
            for key, value in data.items():
                reviewDict[key] = value
            review.delete()
            review.save()
            review = Review(**reviewDict)
            review.save()
            review = storage.get(Review, review.id)
            return jsonify(review.to_dict())
