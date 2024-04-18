#!/usr/bin/python3
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, jsonify, redirect
import json

@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"],  strict_slashes=False)
def user(user_id=None):
    if request.method == "GET":
        if not user_id:
            listUser = []
            users = storage.all(User)
            for user in users.values():
                listUser.append(user.to_dict())
            return jsonify(listUser)
        else:
            user = storage.get(User, user_id)
            if user:
                return jsonify(user.to_dict())
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "DELETE":
        user = storage.get(User, user_id)
        if user:
            storage.delete(user)
            storage.save()
            return jsonify({})
        else:
            return jsonify({"error": "Not found"})
    if request.method == "POST":
        if not user_id:
            try:
                data = request.get_json()
            except:
                response = jsonify({'error': 'Not a JSON'})
                response.status_code = 400
                return response
            if "email" not in data:
                response = jsonify({'error': 'Missing email'})
                response.status_code = 400
                return response
            if "password" not in data:
                response = jsonify({'error': 'Missing password'})
                response.status_code = 400
                return response
            user = User(**data)
            storage.new(user)
            storage.save()
            response = jsonify(user.to_dict())
            response.status_code = 201
            return response
    if request.method == "PUT":
        if user_id:
            user = storage.get(User, user_id)
            if not user:
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
                user = storage.get(User, user_id)
                userDict = user.to_dict()
                for key, value in data.items():
                    userDict[key] = value
                user.delete()
                storage.save()
                user = User(**userDict)
                user.save()
                response = jsonify(user.to_dict())
                response.status_code = 200
                return response
