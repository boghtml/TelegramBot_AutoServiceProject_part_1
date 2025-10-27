import os
from typing import Optional

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

_client: Optional[MongoClient] = None
_db = None

def _get_mongo_uri() -> Optional[str]:
    return os.environ.get('MONGO_URI')

def get_client() -> Optional[MongoClient]:
    """Lazily create and return a MongoClient. Returns None if MONGO_URI is not set."""
    global _client, _db
    if _client is not None:
        return _client

    uri = _get_mongo_uri()
    if not uri:
        print("MONGO_URI not set. Database operations will not work until configured.")
        return None

    try:
        _client = MongoClient(uri, server_api=ServerApi('1'))
        _client.admin.command('ping')
        _db = _client.get_default_database() if _client else None
        print("Connected to MongoDB")
        return _client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        _client = None
        _db = None
        return None

def _get_db():
    global _db
    if _db is not None:
        return _db
    client = get_client()
    if not client:
        raise RuntimeError("MongoDB client not available. Set MONGO_URI environment variable.")

    db = client.get_default_database() if client else client['auto_service']
    _db = db
    return _db

def get_services_base():
    """Return list of services from DB. Raises RuntimeError if DB not configured."""
    db = _get_db()
    return list(db.services.find())

def save_appointment_to_db(user_data):
    """Save appointment and return inserted id string, or None on error."""
    try:
        db = _get_db()
        appointment = {
            "name": user_data.get('name', ''),
            "surname": user_data.get('surname', ''),
            "phone": user_data.get('phone', ''),
            "brand": user_data.get('brand', ''),
            "model": user_data.get('model', ''),
            "year": user_data.get('year', ''),
            "date": user_data.get('date', ''),
            "comment": user_data.get('comment', ''),
            "viewed": False,
            "status": "Очікується"
        }
        result = db.appointments.insert_one(appointment)
        print("Appointment saved with ID:", result.inserted_id)
        return str(result.inserted_id)
    except Exception as e:
        print("Error saving appointment:", e)
        return None

def get_order_info_by_id(order_id):
    try:
        db = _get_db()
        order_info = db.appointments.find_one({'_id': ObjectId(order_id)})
        print("Get_order_info", order_info)
        return order_info
    except Exception as e:
        print(f"Error getting order info by ID: {e}")
        return None

