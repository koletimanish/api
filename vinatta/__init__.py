# Used for Environment
import os

# Flask Setup
from flask import Flask, jsonify

# TODO: CHECK THIS
# Database ORM Layer Setup
from vinatta.db import get_db
db = get_db()

from vinatta.middleware import auth

def create_app(test_config=None):

    #### CONFIG AND SETUP ####
    
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)

    # Configure Flask app
    app.config.from_object('config.default')
    if app.env == 'production':
        app.config.from_object('config.production')
    elif app.env == 'development':
        app.config.from_object('config.development')
    elif test_config is not None:
        app.config.from_mapping(test_config)

    # Connect DB to Flask
    db.init_app(app)

    #### ROUTES #####

    # CORS Headers
    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header['Access-Control-Allow-Headers'] = '*'
        return response
    
    # TODO: Update this to have vinatta specific routes
    # Client Routes
    # from vinatta import client
    # app.register_blueprint(client.bp)

    # Test Route
    @app.route('/hello')
    def hello():
        return 'Hello, Vinatta! 🚀\n'
    
    # Test Authenticated Route
    @app.route('/hello/private')
    @auth.protected_route()
    def hello_private(uid):
        return 'Hello, Vinatta. Shhhhh! 🚀\n'

    return app