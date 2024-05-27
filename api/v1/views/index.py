from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


class_map = {'Amenity': Amenity, 'City': City, 'State': State, 'Place': Place,
             'Review': Review, 'User': User}
cls = ["Amenity", "City", "State", "Place", "Review", "User"]


@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stat():
    tables = storage.table_names()
    all_tables = {}
    for x in range(len(tables)):
        c = cls[x]
        class_name = class_map[c]
        obj = storage.count(class_name)
        all_tables[tables[x]] = obj
    formatted_dict = "{\n"
    for table, count in all_tables.items():
        formatted_dict += f'  "{table}": {count},\n'
    formatted_dict = formatted_dict.rstrip(',\n') + "\n}\n"
    return(formatted_dict)
