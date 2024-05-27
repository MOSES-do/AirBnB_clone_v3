#!/usr/bin/python3
"""routes for web page to access table information"""


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """"return status of request"""
    data = {"status": "OK"}
    res = jsonify(data)
    res.status_code = 200
    return res


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stat():
    """return table name and number of rows"""
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    resp = jsonify(data)
    resp.status_code = 200

    return resp
    """
    tables = storage.table_names()
    all_tables = {}
    for x in range(len(cls)):
        c = cls[x]
        class_name = class_map[c]
        obj = storage.count(class_name)
        all_tables[tables[x]] = obj
    formatted_dict = "{\n"
    for table, count in all_tables.items():
        formatted_dict += f'  "{table}": {count}\n'
    res = formatted_dict.rstrip(',\n') + "\n}\n
    return(res)"""
    """
    class_map = {'Amenity': Amenity, 'City': City,
                 'State': State, 'Place': Place,
             'Review': Review, 'User': User}
    cls = ["Amenity", "City", "State", "Place", "Review", "User"]
    """
