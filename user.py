import const
from database import Database

class User:
    def __init__(self, tg_chat, tg_id, tg_user):
        self.tg_chat = tg_chat
        self.tg_id   = tg_id
        self.tg_user = tg_user

    def to_hash(self):
        return {"tg_chat": self.tg_chat,
                "tg_ud":   self.tg_id,
                "tg_user": self.tg_user}

    def register(self):
        db = Database(const.mongo_server, const.mongo_port)
        return db.insert(const.database_name, const.users_collection, self.to_hash()) 



