import time
import telepot
from telepot.loop import MessageLoop

AVAILABLE_COMMANDS = "/start register your user \n" + \
                     "/stop  unregister your user and delete your devices"

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command
    print msg

    if command == '/start':
        bot.sendMessage(chat_id, 'Welcome to Remote System Control Bot!')
        bot.sendMessage(chat_id, 'These are the available commands')
        bot.sendMessage(chat_id, AVAILABLE_COMMANDS)
    else:
        bot.sendMessage(chat_id, 'Command not recognized')

bot = telepot.Bot('SECRET KEY')

MessageLoop(bot, handle).run_as_thread()

print 'I am listening ...'

while 1:
    time.sleep(10)
