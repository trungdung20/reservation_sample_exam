import pymongo


class Database(object):

    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['hotel_reservation']

    @staticmethod
    def insert(collection, data):
        _id = Database.DATABASE[collection].insert(data)
        return _id

    @staticmethod
    def update(collection, data, query):
        _id = Database.DATABASE[collection].update_one(query, data)
        return _id

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
