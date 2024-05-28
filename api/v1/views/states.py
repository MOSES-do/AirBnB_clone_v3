#!/usr/bin/python3
"""routes for states and get state by id , put, update and delete"""
from flask import jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """get all states from strage"""
    all_states = []
    s = storage.all(State)
    for obj in s.values():
        all_states.append(obj.to_dict())
    return jsonify(all_states)


