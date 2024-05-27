#!/usr/bin/python3
"""routes for states"""


from flask import jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def all_states():
    """list all states from storage"""
    list_state = ""
    s = storage.all(State)
    """id = "1e3c6ba9-8739-452a-b7e4-b82007e76d4f"""
    for key in s:
        list_state += f' {s[key].to_dict()},'
    list_state = list_state.rstrip(',\n') + "}"
    states = f"[{list_state}]"
    return (states)


@app_views.route('/states/<state_id>', methods=['GET'])
def single_state(state_id):
    """list state from storage based on id"""
    s = storage.all(State)
    for key, value in s.items():
        if value.id == state_id:
            return(value.to_dict())
        else:
            abort(404, description="State not found")
