import const
from command import Command
from database import Database

class Device:
    def __init__(self, user, device_id=None):
        self.device_id  = device_id
        self.user       = user

    def add(self, chat_id, text):
        command = Command(self.user)

        if command.command != "/add":
            const.bot.sendMessage(chat_id, 'Tell me the name of the device')
            device_id = self.create()
            command.update("/add", 0, 0, device_id)
        else:
            element = command.element

            if command.status == 0:
                const.bot.sendMessage(chat_id, 'Tell me the IP of the device')
                self.update(command.element, {"name": text})
                command.update("/add", 1, 0, element)
            elif command.status == 1:
                const.bot.sendMessage(chat_id, 'Tell me the ssh port')
                self.update(command.element, {"ip": text})
                command.update("/add", 2, 0, element)
            elif command.status == 2:
                const.bot.sendMessage(chat_id, 'Tell me the ssh user')
                self.update(command.element, {"port": text})
                command.update("/add", 3, 0, element)
            elif command.status == 3:
                self.update(command.element, {"user": text})
                const.bot.sendMessage(chat_id, 'Device sucessfully created')

                device = Device.get_by_id(command.element)

                const.bot.sendMessage(chat_id, 'Name: ' + device['name'])
                const.bot.sendMessage(chat_id, 'IP: ' + device['ip'])
                const.bot.sendMessage(chat_id, 'SSH port: ' + device['port'])
                const.bot.sendMessage(chat_id, 'SSH user: ' + device['user'])

                command.update("device created")

                del device

        del command

    def default(self):
        return {"user": self.user, "device_id": "", "ip": "", "name": "", "port": "", "ssh_private": "", "ssh_public": ""}

    def create(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.insert(const.database_name, const.devic_collection, self.default())

        del db

        return ret

    @staticmethod
    def get_by_id(_id):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.get_single(const.database_name, const.devic_collection, {"_id": _id})

        del db

        return ret

    def update(self, _id, data):
        db = Database(const.mongo_server, const.mongo_port)
        db.update(const.database_name, const.devic_collection, {"_id": _id}, data)

        del db
