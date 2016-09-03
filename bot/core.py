#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import Libraries
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import json
import pprint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def psi3hour(bot, update):

    # Make the HTTP request.
    headers = {'api-key': 'zK5ZrvAN6v4GLUsWGpjgUFJs6Ztj17n6'}
    r = requests.get('https://api.data.gov.sg/v1/environment/psi', headers=headers)

    # Load data into Dictionary and get reading
    data = json.loads(r.text)
    hourly = data['items'][0]['readings']['psi_three_hourly']

    # Create Response
    final_string = "The 3 hourly PSI Reading is actually \n\n"
    for key in hourly:
        final_string  =  final_string + (str(key) + " " + str(hourly[key]) + "\n")
    bot.sendMessage(update.message.chat_id, text=final_string)

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello! I am @ShiokBot! \n The helpful singlish spouting bot!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello! I am @ShiokBot! \n The helpful singlish spouting bot!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("231443961:AAEwNQmrWUDYzDNC9hEmeyRgUPr61ruDqS0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("psi", psi3hour))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
