from pymongo import MongoClient

class Database:
    def __init__(self, server, port):
        self.server = server
        self.port   = port

    def exists(self, database, collection, element_key):
        client, co = self.__create_objects(database, collection)
        ret_element = co.find(element_key)

        client.close()

        Database.delete_objects(client, co)

        try:
            ret_element.next()

            return True
        except StopIteration:
            return False
        finally:
            del ret_element

    def get_single(self, database, collection, element_key):
        client, co = self.__create_objects(database, collection)
        ret_element = co.find(element_key)

        client.close()

        Database.delete_objects(client, co)

        try:
            return ret_element.next()
        except StopIteration:
            return None
        finally:
            del ret_element

    def insert(self, database, collection, data):
        client, co = self.__create_objects(database, collection)
        ret_id = co.insert(data)

        client.close()

        Database.delete_objects(client, co)

        return ret_id

    def update(self, database, collection, element_key, data):
        client, co = self.__create_objects(database, collection)
        ret_id = co.update(element_key, {"$set": data})

        client.close()

        Database.delete_objects(client, co)

        return ret_id

    #------------------------------------------------------
    # PRIVATE METHODS
    #------------------------------------------------------

    def __create_objects(self, database, collection):
        ret_client = MongoClient(self.server, self.port)
        ret_co = ret_client[database][collection]

        return ret_client, ret_co

    @staticmethod
    def delete_objects(client, co):
        del co
        del client

    #-----------------------------------------------------#
