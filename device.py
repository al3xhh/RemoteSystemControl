import const
from command import Command
from database import Database

class Device:
    def __init__(self, user, name=None):
        self.user = user
        self.name = name

        if name:
            self.update_att()

    #-------------------------------
    # Add a new device to the system
    #-------------------------------
    def add(self, text):
        command = Command(self.user)

        if command.command != "/add":
            ret = 'What is the name of the device?'
            device_id = self.create()
            command.update("/add", 0, 0, device_id)
        else:
	    device_id = command.element
            command.update("/add", command.status + 1, 0, device_id)

            if command.status == 0:
		ret = 'What is the IP of the device?'
		self.update(command.element, {"name": text})
	    elif command.status == 1:
		ret = 'What is the SSH port?'
		self.update(command.element, {"ip": text})
	    elif command.status == 2:
		ret = 'What is the SSH user?'
		self.update(command.element, {"ssh_port": text})
	    elif command.status == 3:
		self.update(command.element, {"ssh_user": text})
		ret = 'Device sucessfully created!'
                command.update("device created")

        del command

        return ret

    #----------------------------------
    # Create the device in the database
    #----------------------------------
    def create(self):
        db = Database(const.mongo_server, const.mongo_port)
        ret = db.insert(const.database_name, const.devic_collection, self.default())

        del db

        return ret

    #-----------------------------------------------------------
    # Get default device hash
    #   - ip:           ip direction of the device
    #   - name:         name of the device (it's unique)
    #   - ssh_port:     sshd port
    #   - ssh_private:  ssh private key to access to the device
    #   - ssh_public:   ssh public key to access to the device
    #   - ssh_user:     ssh user to access to the device
    #-----------------------------------------------------------
    def default(self):
	return {"user"          : self.user,
                "ip"            : "",
                "name"          : "",
                "ssh_port"      : "",
                "ssh_private"   : "",
                "ssh_public"    : "",
                "ssh_user"      : ""}

    #-------------------------------------------
    # Get a device using its name and owner user
    #-------------------------------------------
    def get_by_name(self):
	db = Database(const.mongo_server, const.mongo_port)
	ret = db.get_single(const.database_name, const.devic_collection, {"name": self.name, "user": self.user})

	del db

        if not ret:
            raise Exception('Device not found')

	return ret

    #-------------
    # List devices
    #-------------
    def list(self):
        db = Database(const.mongo_server, const.mongo_port)
        devices = db.get(const.database_name, const.devic_collection, {"user": self.user})

        del db

        ret = ''

        if devices.count() > 0:
            for device in devices:
                ret += device['name'] + ' ' + device['ip'] + "\n"
        else:
            ret = 'There are no devices'

        return ret

    #------------------------
    # Show device information
    #------------------------
    def show(self):
	return 'name: '     + self.name     + "\n" \
               'ip: '       + self.ip       + "\n" \
               'ssh port: ' + self.ssh_port + "\n" \
               'ssh user: ' + self.ssh_user

    #----------------------------------
    # Update the device in the database
    #----------------------------------
    def update(self, _id, data):
	db = Database(const.mongo_server, const.mongo_port)
	db.update(const.database_name, const.devic_collection, {"_id": _id}, data)

	del db

    #--------------------------
    # Update objects attributes
    #--------------------------
    def update_att(self):
	device = self.get_by_name()

	self.user          = device['user']
	self.ip            = device['ip']
	self.ssh_port      = device['ssh_port']
	self.ssh_private   = device['ssh_private']
	self.ssh_public    = device['ssh_public']
	self.ssh_user	   = device['ssh_user']

	del device
