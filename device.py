import const
from command import Command
from database import Database

class Device:
    def __init__(self, user, name=None):
        self.user = user
        self.name = name

        if name != None:
            self.update_att()


    def add(self, chat_id, text):
        command = Command(self.user)

        if command.command != "/add":
            const.bot.sendMessage(chat_id, 'Tell me the name of the device')
            device_id = self.create()
            command.update("/add", 0, 0, device_id)
        else:
	    device_id = command.element

            if command.status == 0:
		const.bot.sendMessage(chat_id, 'Tell me the IP of the device')
		self.update(command.element, {"name": text})
		command.update("/add", 1, 0, device_id)
	    elif command.status == 1:
		const.bot.sendMessage(chat_id, 'Tell me the ssh port')
		self.update(command.element, {"ip": text})
		command.update("/add", 2, 0, device_id)
	    elif command.status == 2:
		const.bot.sendMessage(chat_id, 'Tell me the ssh user')
		self.update(command.element, {"ssh_port": text})
		command.update("/add", 3, 0, device_id)
	    elif command.status == 3:
		self.update(command.element, {"ssh_user": text})
		const.bot.sendMessage(chat_id, 'Device sucessfully created')

                device = Device.get_by_id(command.element)
		device = Device(device['user'], device['name'])
		device.show(chat_id)

                command.update("device created")

		del device

        del command

    def default(self):
	return {"user": self.user, "ip": "", "name": "", "ssh_port": "", "ssh_private": "", "ssh_public": "", "ssh_user": ""}

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

    def get_by_name(self):
	db = database(const.mongo_server, const.mongo_port)
	ret = db.get_single(const.database_name, const.devic_collection, {"name": self.name, "user": self.user})

	del db

	return ret

    def update_att(self):
	device = self.get_by_name()

	self.user          = device['user']
	self.ip            = device['ip']
	self.ssh_port      = device['ssh_port']
	self.ssh_private   = device['ssh_private']
	self.ssh_public    = device['ssh_public']
	self.ssh_user	   = device['ssh_user']

	del device

    def update(self, _id, data):
	db = database(const.mongo_server, const.mongo_port)
	db.update(const.database_name, const.devic_collection, {"_id": _id}, data)

	del db

    def show(self, chat_id):
	const.bot.sendmessage(chat_id, 'name: ' + self.name + "\n" \
                                       'ip: ' + self.ip + "\n" \
                                       'ssh port: ' + self.ssh_port + "\n" \
                                       'ssh user: ' + self.ssh_user)
