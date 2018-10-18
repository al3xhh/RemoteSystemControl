from pymongo import MongoClient

class Database:
    def __init__(self, server, port):
        self.server = server
        self.port   = port

    def insert(self, database, collection, data):
        client = MongoClient(self.server, self.port)
        db = client.database
        co = db.collection

        post_id = co.insert(data)

        client.close()

        return post_id
