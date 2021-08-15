from django.conf import settings
import logging


def get_database(name="default"):
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "{PROTOCOL}://{USER}:{PASSWORD}@{HOST}/".format(
        **settings.MONGODB.get(name)
    )
    logging.debug("Mongodb Connection String %s", CONNECTION_STRING)
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient

    client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client[settings.MONGODB.get(name)["NAME"]]


def get_collection(collection_name, database_name="default"):
    return get_database(name=database_name)[collection_name]


class MongoModel:
    COLLECTION = "articles"
    ID_KEY = "_id"
    INDEX = None
    _data = None

    def __init__(self, **kwargs):
        self._data = kwargs

    def get_value(self):
        return self._data

    def get_key(self, **kwargs):
        return self._data[self.ID_KEY]

    @classmethod
    def get(cls, key):
        obj = get_collection(cls.COLLECTION).find_one({cls.ID_KEY: key})
        return cls(**obj)

    def save(self, **kwargs):
        value = self.get_value()

        key = value[self.ID_KEY] = self.get_key(**value)
        collection = get_collection(self.COLLECTION)
        res = collection.update({self.ID_KEY: key}, value, True)
        assert "ok" in res
        if self.INDEX:
            collection.create_index(list(self.INDEX.items()))

        return value

    @classmethod
    def search(cls, query, limit=10, offset=0):
        for obj in (
            get_collection(cls.COLLECTION)
            .find({"$text": {"$search": query}})
            .skip(offset)
            .limit(limit)
        ):
            logging.debug("search result %s", obj)
            yield cls(**obj)

    def delete(self):
        get_collection(self.COLLECTION).delete_one(
            {self.ID_KEY: self.get_key()}
        )
