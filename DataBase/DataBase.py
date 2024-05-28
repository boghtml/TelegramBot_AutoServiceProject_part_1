from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://boghtml:1234567890HTML@cluster0.prceocq.mongodb.net/auto_service?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['auto_service']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def get_services_base():
    return list(db.services.find())

def save_appointment_to_db(user_data):
    try:
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
        # Збереження запису в базу даних
        result = db.appointments.insert_one(appointment)
        print("Appointment saved with ID:", result.inserted_id)  # Виводимо ID
        return str(result.inserted_id)  # Повертаємо строкове представлення ID
    except Exception as e:
        print("Error saving appointment:", e)
        return None

from bson import ObjectId

def get_order_info_by_id(order_id):
    try:
        order_info = db.appointments.find_one({'_id': ObjectId(order_id)})
        print("Get_order_info", order_info)
        return order_info
    except Exception as e:
        print(f"Error getting order info by ID: {e}")
        return None

