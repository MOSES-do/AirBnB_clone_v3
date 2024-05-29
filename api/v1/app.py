#!/usr/bin/python3
"""register blueprint of routes to main application"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

storage_t = os.environ.get('HBNB_TYPE_STORAGE')
host = os.environ.get('HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', 5000)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """close database connection after session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """return 404 error on page not found"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host, port)
