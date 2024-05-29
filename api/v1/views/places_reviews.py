#!/usr/bin/python3
"""routes for states and get state by id , put, update and delete"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False,
                 endpoint='all_reviews')
def all_reviews(place_id):
    """get all places from storage"""
    all_reviews = []
    entity = storage.get(Place, place_id)
    if entity is None:
        abort(404)
    for review in entity.reviews:
        all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False,
                 endpoint='single_review')
def single_review(review_id):
    """return review based on id"""
    s = storage.all(Review)
    for key, value in s.items():
        if value.id == review_id:
            return jsonify(value.to_dict())
    abort(404, description="State not found")


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False,
                 endpoint='update_review')
def update_review(review_id):
    """
    updates specific State object by ID
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    found_obj = storage.get(Review, str(review_id))
    if found_obj is None:
        abort(404)
    for key, val in review_json.items():
        """
        cond: below is a key exclusion to ensure
        id, created_at & updated_at don't get updated
        """
        if key not in ["id", "created_at", "updated_at", "user_id"]:
            setattr(found_obj, key, val)
    found_obj.save()
    return jsonify(found_obj.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False,
                 endpoint='del_review')
def del_review(review_id):
    """delete review based on id"""
    entity = storage.get(Review, review_id)
    if entity is None:
        abort(404, description="State not found")
    storage.delete(entity)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False,
                 endpoint='create_review')
def create_review(place_id):
    """
    return: newly created review obj
    """
    review_json = request.get_json(silent=True)

    if review_json is None:
        abort(400, 'Not a JSON')
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing name')
    if not storage.get(User, review_json["user_id"]):
        abort(404)
    if not storage.get(Place, review_id):
        abort(404)

    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    new_review.save()
    res = jsonify(new_.to_review.to_dict())
    res.status_code = 201

    return res
~                                                                                                                                                   ~                                                                                                                                                   ~                   
