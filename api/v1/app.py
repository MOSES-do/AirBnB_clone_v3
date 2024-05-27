from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

storage_t = os.environ.get('HBNB_TYPE_STORAGE')
host = os.environ.get('HOST')
port = os.environ.get('HBNB_API_PORT')

"""if storage_t == 'db':"""
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host, port)
