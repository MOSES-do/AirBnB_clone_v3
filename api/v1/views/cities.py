#!/usr/bin/python3
"""routes for states and get state by id , put, update and delete"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False,
                 endpoint='all_cities')
def all_cities(state_id):
    """get all cities of a state from storage"""
    all_cities = []
    entity = storage.get(State, state_id)
    if entity is None:
        abort(404)
    for city in entity.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False,
                 endpoint='single_city')
def single_city(city_id):
    """return state based on id"""
    s = storage.all(City)
    for key, value in s.items():
        if value.id == city_id:
            return jsonify(value.to_dict())
    abort(404, description="State not found")


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False,
                 endpoint='city_create')
def city_create(state_id):
    """
    return: newly created state obj
    """
    entity = storage.get(State, state_id)
    city_json = request.get_json(silent=True)
    if entity is None:
        abort(404)
    if city_json is None:
        abort(400, 'Not a JSON')
    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id
    new_city = City(**city_json)
    new_city.save()
    res = jsonify(new_city.to_dict())
    res.status_code = 201

    return res


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False,
                 endpoint='del_city')
def del_city(city_id):
    """delete city based on id"""
    entity = storage.get(City, city_id)
    if entity is None:
        abort(404, description="State not found")
    storage.delete(entity)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=False,
                 endpoint='update_city')
def update_city(city_id):
    """
    updates specific State object by ID
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    found_obj = storage.get(City, str(city_id))
    if found_obj is None:
        abort(404)
    for key, val in city_json.items():
        """
        cond: below is a key exclusion to ensure
        id, created_at & updated_at don't get updated
        """
        if key not in ["id", "created_at", "updated_at"]:
            setattr(found_obj, key, val)
    found_obj.save()
    return jsonify(found_obj.to_dict())
