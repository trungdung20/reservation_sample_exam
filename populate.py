import pymongo
from pymongo import MongoClient
from datetime import datetime
from models.consts import *
import uuid

client = MongoClient('localhost', 27017)
database = client["hotel_reservation"]

permission_ids = ["0b9f0a17d4c841a8bcefed2869e925e7", "33a6cbbcbf864d90acf0e7d7f5d59082", "6cc0c65ecc274461a0f9c69324d489fb"]

def insert_permission():
    permission_names = [PERMISSION_INVENTORY_ADD, PERMISSION_VIEW_INVETORY,
        PERMISSION_ACCOMMODATION_ADD, PERMISSION_HOTEL_ADD, PERMISSION_RESERVATION_VIEW,
        PERMISSION_RESERVATION_CONFIRM]
    permissions = []
    for name in permission_names:
        permission = {
            "_id" : uuid.uuid4().hex,
            "name": name.strip(),
            "create_time" : datetime.utcnow(),
            "update_time" : None
        }
        permissions.append(permission)

    ids = database[PERMISSION_COLLECTION].insert_many(permissions)

    return ids.inserted_ids

def insert_role(permission_ids):
    role = {
        "_id" : uuid.uuid4().hex,
        "name" : "superuser",
        "permissions" : permission_ids,
        "create_at": datetime.utcnow(),
        "update_at": None
    }

    id = database[ROLE_COLLECTION].insert(role)
    return id

def insert_superuser(role_id):

    user = {
        "first_name": "John",
        "last_name" : "William",
        "email": "john1990@gmail.com",
        "password": "password101",
        "role_id" : role_id,
        "superuser" : True,
        "create_at": datetime.utcnow(),
        "update_at": None
    }
    id = database[USER_COLLECTION].insert_one(user)
    return id

def insert_hotel():
    pass



if __name__ == "__main__":
    insert_permission()