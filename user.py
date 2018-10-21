import const
from database import Database

class User:
    def __init__(self, tg_chat, tg_id, tg_user):
        self.tg_chat = tg_chat
        self.tg_id   = tg_id
        self.tg_user = tg_user
        self.id      = self.get()['_id']

    def to_hash(self):
        return {"tg_chat": self.tg_chat,
                "tg_id":   self.tg_id,
                "tg_user": self.tg_user}

    def register(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.insert(const.database_name, const.users_collection, self.to_hash())

        del db

        return ret

    def exists(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.exists(const.database_name, const.users_collection, {"tg_id": self.tg_id})

        del db

        return ret

    def get(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.get_single(const.database_name, const.users_collection, {"tg_id": self.tg_id})

        del db

        return ret
