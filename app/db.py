from flask import current_app
from pymongo import MongoClient
from urllib.parse import quote_plus

def init_db(app):
    """Initialize the database connection."""
    # Credentials
    username = "kyadavalli04"
    password = "Kousthubh%40mongodb"

    

    # MongoDB URI
    mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.2o0bzi6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true"
    
    # Initialize MongoDB client and database
    client = MongoClient(mongo_uri)
    app.db = client['dimensionless_todo_list']  
