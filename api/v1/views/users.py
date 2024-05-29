#!/usr/bin/python3
"""routes for amenities"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False, endpoint='all_users')
def all_users():
    """get all states from strage"""
    all_users = []
    s = storage.all(User)
    for obj in s.values():
        all_users.append(obj.to_dict())
    return jsonify(all_users)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False, endpoint='create_user')
def create_user():
    """
    :return: newly created amenity obj
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in state_json:
        abort(400, 'Missing email')
    if "password" not in state_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    res = jsonify(new_user.to_dict())
    res.status_code = 201

    return res

@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False, endpoint='single_user')
def single_user(user_id):
    """return state based on id"""
    s = storage.all(User)
    for key, value in s.items():
        if value.id == user_id:
            return jsonify(value.to_dict())
    abort(404, description="State not found")


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False, endpoint='update_user')
def update_amenity(user_id):
    """
    update user object by ID
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    for key, val in user_json.items():
        """
        cond: below is a key exclusion to ensure
        id, created_at & updated_at don't get updated
        """
        if key not in ["id", "email",  "created_at", "updated_at"]:
            setattr(user_obj, key, val)
    amenity_obj.save()
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='del_user')
def del_user(user_id):
    """delete user based on id"""
    entity = storage.get(User, str(user_id))
    if entity is None:
        abort(404, description="State not found")
    storage.delete(entity)
    storage.save()
    return jsonify({})
