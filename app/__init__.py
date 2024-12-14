from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__, template_folder='templates')  # Ensure static folder is set correctly
    CORS(app)
    from app.db import init_db
    from app.routes import register_routes

    # Initialize 
    init_db(app)
    
    # Register routes
    register_routes(app)

    return app
