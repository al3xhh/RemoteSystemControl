import const
from database import Database

class Command:
    def __init__(self, user):
        self.user = user
        command = self.get()

        if command == None:
            self.create()

        self.update_att()

    def default(self):
        return {"user": self.user, "command": "", "status": 0, "cancel_status": 0, "element": 0}

    def create(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.insert(const.database_name, const.lastc_collection, self.default())

        del db

        return ret

    def get(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.get_single(const.database_name, const.lastc_collection, {"user": self.user})

        del db

        return ret

    def update_att(self):
        command = self.get()

        self.command       = command['command']
        self.status        = command['status']
        self.cancel_status = command['cancel_status']
        self.user          = command['user']
        self.element       = command['element']

    def update(self, command, status=0, cancel_status=0, element=0):
        db = Database(const.mongo_server, const.mongo_port)
        db.update(const.database_name, const.lastc_collection, {"user": self.user}, {"command"       : command,
                                                                                     "status"        : status,
                                                                                     "cancel_status" : cancel_status,
                                                                                     "element"       : element})
        del db
