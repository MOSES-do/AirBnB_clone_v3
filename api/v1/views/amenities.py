#!/usr/bin/python3
"""routes for amenities"""
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False, endpoint='all_amenities')
def all_amenities():
    """get all states from strage"""
    all_amenitys = []
    s = storage.all(Amenity)
    for obj in s.values():
        all_amenitys.append(obj.to_dict())
    return jsonify(all_amenitys)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False, endpoint='create_amenity')
def create_amenity():
    """
    :return: newly created amenity obj
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    res = jsonify(new_amenity.to_dict())
    res.status_code = 201

    return res


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False, endpoint='single_amenity')
def single_amenity(amenity_id):
    """return state based on id"""
    s = storage.all(Amenity)
    for key, value in s.items():
        if value.id == amenity_id:
            return jsonify(value.to_dict())
    abort(404, description="State not found")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False, endpoint='update_amenity')
def update_amenity(amenity_id):
    """
    updates specific Amenity object by ID
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    for key, val in amenity_json.items():
        """
        cond: below is a key exclusion to ensure
        id, created_at & updated_at don't get updated
        """
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, val)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='del_amenity')
def del_amenity(amenity_id):
    """delete state based on id"""
    entity = storage.get(Amenity, str(amenity_id))
    if entity is None:
        abort(404, description="State not found")
    storage.delete(entity)
    storage.save()
    return jsonify({})
