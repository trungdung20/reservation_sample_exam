from service.database import Database
from models.base import BaseModel
from models.consts import *
from flask import session


class User(BaseModel):
    def __init__(self, _id, first_name, last_name, email, superuser, password, create_time=None, update_time=None):
        super(User, self).__init__(_id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.superuser = superuser
        self.password = password
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "superuser": self.superuser,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def find_user(email):
        user = User.find_one(USER_COLLECTION, {"email" : email})
        return User(**user)

    @staticmethod
    def login_validation(email, password):
        user = User.find_one(USER_COLLECTION, query={"email": email, "password": password})
        if user is not None:
            return True
        return False

    @classmethod
    def register(cls, first_name, last_name, email, superuser, password, role_type):
        user = cls.find_one(USER_COLLECTION, query={"email": email})
        if user is None:
            try:
                new_user = cls(None, first_name, last_name, email, superuser, password)
                user_id = new_user.create(USER_COLLECTION)
                permissions = ROLE_TO_PERMISSION_MAPPING[role_type]
                results = Permission.find(PERMISSION_COLLECTION, {"name": {"$in": permissions}})
                permission_ids = [result["_id"] for result in results]

                role = Role(None, user_id, first_name + "_" + str(ROLE_ENUM[role_type]), permission_ids)
                role.create(ROLE_COLLECTION)
                return True
            except:
                return False
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None



class Role(BaseModel):
    def __init__(self, _id, user_id, name, permission_ids, create_time=None, update_time=None):
        super(Role, self).__init__(_id)
        self.name = name
        self.user_id = user_id
        self.permission_ids = permission_ids
        self.create_time = create_time
        self.update_time = update_time

    @staticmethod
    def get_role(user_id):
        role = Database.find_one(ROLE_COLLECTION, {"user_id": user_id})

        if role:
            return Role(**role)
        return None

    def find_permissions(self):
        results = Permission.find(PERMISSION_COLLECTION, {"_id": {"$in": self.permission_ids}})
        return results

    def to_json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "permission_ids": self.permission_ids,
        }


class Permission(BaseModel):
    def __init__(self, _id, name, create_time=None, update_time=None):
        super(Permission, self).__init__(_id)
        self.name = name
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "name": self.name
        }
