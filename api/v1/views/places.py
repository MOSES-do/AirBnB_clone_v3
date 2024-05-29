#!/usr/bin/python3
"""routes for states and get state by id , put, update and delete"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False,
                 endpoint='all_places')
def all_places(city_id):
    """get all places from storage"""
    all_places = []
    entity = storage.get(City, city_id)
    print(entity)
    if entity is None:
        abort(404)
    for place in entity.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False,
                 endpoint='single_place')
def single_place(place_id):
    """return place based on id"""
    s = storage.all(Place)
    for key, value in s.items():
        if value.id == place_id:
            return jsonify(value.to_dict())
    abort(404, description="State not found")


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False,
                 endpoint='update_place')
def update_place(place_id):
    """
    updates specific State object by ID
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    found_obj = storage.get(Place, str(place_id))
    if found_obj is None:
        abort(404)
    for key, val in place_json.items():
        """
        cond: below is a key exclusion to ensure
        id, created_at & updated_at don't get updated
        """
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(found_obj, key, val)
    found_obj.save()
    return jsonify(found_obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False,
                 endpoint='del_place')
def del_city(place_id):
    """deleteplace based on id"""
    entity = storage.get(Place, place_id)
    if entity is None:
        abort(404, description="State not found")
    storage.delete(entity)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False,
                 endpoint='place_create')
def place_create(city_id):
    """
    return: newly created state obj
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')
    if not storage.get(User, place_json["user_id"]):
        abort(404)
    if not storage.get(City, city_id):
        abort(404)

    place_json["city_id"] = city_id
    new_place = Place(**place_json)
    new_place.save()
    res = jsonify(new_place.to_dict())
    res.status_code = 201

    return res
