#!/usr/bin/python3
"""routes for states and get state by id , put, update and delete"""
from flask import jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    all_states = []
    s = storage.all(State)
    """id = "1e3c6ba9-8739-452a-b7e4-b82007e76d4f"""
    for obj in s.values():
        all_states.append(obj.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def single_state(state_id):
    s = storage.all(State)
    for key, value in s.items():
        if value.id == state_id:
            return(value.to_dict())
        else:
            abort(404, description="State not found")
