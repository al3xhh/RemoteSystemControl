import time
import telepot
from telepot.loop import MessageLoop

from user import User
import const

def init_constants():
    const.available_commands = "/start register your user \n" + \
        	               "/stop  unregister your user and delete your devices"

    const.mongo_server = '10.0.0.6'
    const.mongo_port = 27017

    const.database_name = "rsc_bot"

    const.users_collection = "rsc_bot_users"

    const.bot = telepot.Bot('SECRET')

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command
    print msg

    if command == '/start':
        const.bot.sendMessage(chat_id, 'Welcome to Remote System Control Bot!')
        const.bot.sendMessage(chat_id, 'These are the available commands')
        const.bot.sendMessage(chat_id, const.available_commands)
	const.bot.sendMessage(chat_id, 'Registering user...')

	user = User(chat_id, msg['from']['id'], msg['from']['username'])
	user_id = user.register()

	const.bot.sendMessage(chat_id, 'User registered with ID:' + str( user_id))
	const.bot.sendMessage(chat_id, 'Welcome ' + user.tg_user + '!')

	del user 
    else:
        const.bot.sendMessage(chat_id, 'Command not recognized')

def main():
    init_constants()

    MessageLoop(const.bot, handle).run_as_thread()

    print 'I am listening ...'

    while 1:
        time.sleep(10)

main()
