#!/usr/bin/python3
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import request, jsonify, redirect
import json

@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"],  strict_slashes=False)
def state(state_id=None):
    if request.method == "GET":
        if not state_id:
            listState = []
            states = storage.all(State)
            for state in states.values():
                listState.append(state.to_dict())
            return jsonify(listState)
        else:
            state = storage.get(State, state_id)
            if state:
                return jsonify(state.to_dict())
            else:
                response = jsonify({"error": "Not found"})
                response.status_code = 404
                return response
    if request.method == "DELETE":
        state = storage.get(State, state_id)
        if state:
            storage.delete(state)
            storage.save()
            return jsonify({})
        else:
            return jsonify({"error": "Not found"})
    if request.method == "POST":
        if not state_id:
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
            state = State(**data)
            storage.new(state)
            storage.save()
            response = jsonify(state.to_dict())
            response.status_code = 201
            return response
    if request.method == "PUT":
        if state_id:
            state = storage.get(State, state_id)
            if not state:
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
                state = storage.get(State, state_id)
                stateDict = state.to_dict()
                for key, value in data.items():
                    stateDict[key] = value
                state.delete()
                storage.save()
                state = State(**stateDict)
                state.save()
                response = jsonify(state.to_dict())
                response.status_code = 200
                return response
