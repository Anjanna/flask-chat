from pymongo.mongo_client import MongoClient

class ChatSession:
    def __init__(self, db_name):
        self.__mongo_client = None
        self.db_name = db_name
        self.__doc_client = None

    @property
    def mongo_client(self):
        if not self.__mongo_client:
            self.__mongo_client = self._create_mongo_client()
        return self.__mongo_client

    @property
    def doc_client(self):
        if self.__doc_client is None:
            self.__doc_client = self.mongo_client[self.db_name]
        return self.__doc_client

    def _create_mongo_client(self):
        uri = "mongodb+srv://admin:Admin123@cluster0.ydmkr9s.mongodb.net/?retryWrites=true&w=majority"
        return MongoClient(uri, tlsInsecure=True)

    def ping_db(self):
        return self.mongo_client.admin.command('ping')

    def insert_one(self, data, collection):
        return self.doc_client[collection].insert_one(data)

    def find_one(self, filter_query, collection):
        return self.doc_client[collection].find_one(filter_query)
