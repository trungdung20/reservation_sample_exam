import uuid
from service.database import Database
import datetime

class BaseModel(object):

    Database = Database

    def __init__(self, _id):
        self._id = uuid.uuid4().hex if _id is None else str(_id)

    def create(self, collection_name):
        data = self.to_json()
        data['create_time'] = datetime.datetime.utcnow()
        return Database.insert(collection=collection_name,
                        data=data)

    def update(self, collection_name, query):
        data = self.to_json()
        data['update_time'] = datetime.datetime.utcnow()
        return Database.update(collection=collection_name, query=query, data={"$set" : data})

    def to_json(self):
        pass

    @classmethod
    def get_one_by_id(cls, collection_name, id):
        result = Database.find_one(collection=collection_name, query={'_id': id})
        return cls(**result).to_json()

    @classmethod
    def get_all(cls, collection_name):
        results = Database.find(collection=collection_name,
                              query={})
        return [cls(**result).to_json() for result in results]

    @classmethod
    def find(cls, collection_name, query):
        results = Database.find(collection=collection_name,
                                query=query)
        results = [cls(**result).to_json() for result in results]

        return results

    @classmethod
    def find_one(cls, collection_name, query):
        result = Database.find_one(collection=collection_name,
                                query=query)
        if result:
            return cls(**result).to_json()

        return None