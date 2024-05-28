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


@app_views.route(
                '/states/<state_id>', methods=['GET']
                strict_slashes=False
                )
def single_state(state_id):
    """return state based on id"""
    s = storage.all(State)
    for key, value in s.items():
        if value.id == state_id:
            return(value.to_dict())
        else:
            abort(404, description="State not found")


@app_views.route(
                '/states/<state_id>', methods=['DELETE'],
                strict_slashes=False
                )
def single_state(state_id):
    """delete state based on id"""
    entity = storage.get(State, str(state_id))
    if entity is None:
        abort(404, description="State not found")
    storage.delete(entity)
    storage.save()
    return jsonify({})


@app_views.route(
                "/states/<state_id>",  methods=["PUT"],
                strict_slashes=False
                )
def state_put(state_id):
    """
    updates specific State object by ID
    return: state object and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    found_obj = storage.get("State", str(state_id))
    if found_obj is None:
        abort(404)
    for key, val in state_json.items():
        """
        cond: below is a key exclusion to ensure
        id, created_at & updated_at don't get updated
        """
        if key not in ["id", "created_at", "updated_at"]:
            setattr(found_obj, key, val)
    found_obj.save()
    return jsonify(found_obj.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    return: newly created state obj
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    res = jsonify(new_state.to_dict())
    res.status_code = 201

    return res
