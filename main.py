import time
import telepot
from telepot.loop import MessageLoop

from command import Command
from device import Device
from user import User
import const

def init_constants():
    const.available_commands = "/start register your user \n" + \
                               "/stop unregister your user \n" + \
                               "/add add a new device \n" + \
                               "/delete <id> delete a device \n" + \
                               "/update <id> update a device \n" + \
                               "/list list the devices \n" + \
                               "/device_show <id> show device info \n" + \
                               "/monit <id> monitor a device \n" + \
                               "/poweroff <id> power off a device \n" + \
                               "/reboot <id> rebot a device \n" + \
                               "/poweron <id> power on a device \n" + \
                               "/execute <cmd> <id> execute cmd on the device \n" + \
                               "/groups list the devices groups \n" + \
                               "/group <cmd> <id> execute cmd on group devices \n" + \
                               "/group_show <id> show devices in the group \n" + \
                               "/help show this list \n" + \
                               "/help <command> show command help"

    const.mongo_server = '10.0.0.6'
    const.mongo_port = 27017

    const.database_name = "rsc_bot"

    const.users_collection = "rsc_bot_users"
    const.lastc_collection = "rsc_bot_last_command"
    const.devic_collection = "rsc_bot_devices"

    const.bot = telepot.Bot('SECRET')

def handle(msg):
    command = msg['text']

    print 'Got command: %s' % command
    print msg

    user = User(msg['chat']['id'], msg['from']['id'], msg['from']['username'])
    last_command = Command(user.id)

    if command == '/start':
        if not user.exists():
            const.bot.sendMessage(user.tg_chat, 'Welcome to Remote System Control Bot!')
            const.bot.sendMessage(user.tg_chat, 'These are the available commands')
            const.bot.sendMessage(user.tg_chat, const.available_commands)
            const.bot.sendMessage(user.tg_chat, 'Registering user...')

            user_id = user.register()

            const.bot.sendMessage(user.tg_chat, 'User registered with ID:' + str(user_id))
            const.bot.sendMessage(user.tg_chat, 'Welcome ' + user.tg_user + '!')
        else:
            const.bot.sendMessage(user.tg_chat, 'User ' + user.tg_user + ' is already registered!')

        last_command.update("/start")
    elif command == '/add' or last_command.command == '/add':
        device = Device(user.id)
        device.add(user.tg_chat, command)

        del device
    elif command == '/help':
        const.bot.sendMessage(user.tg_chat, const.available_commands)
        user_command.update("/help")
    else:
        const.bot.sendMessage(user.tg_chat, 'Command not recognized')
        last_command.update(command)

    del user
    del last_command

def main():
    init_constants()

    MessageLoop(const.bot, handle).run_as_thread()

    print 'I am listening ...'

    while 1:
        time.sleep(10)

main()
