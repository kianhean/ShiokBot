#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# Import Libraries
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import json
import os

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
    timestampp = data['items'][0]['timestamp'][:19].replace("T"," ")

    # Create Response
    final_string = "The 3 hourly PSI Reading at " + timestampp + " is actually \n\n"
    for key in sorted(hourly):
        final_string  =  final_string + (str(key) + " " + str(hourly[key]) + "\n")
    bot.sendMessage(update.message.chat_id, text=final_string)


def weathernow(bot, update):
    headers = {'api-key': 'zK5ZrvAN6v4GLUsWGpjgUFJs6Ztj17n6'}
    r = requests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast', headers=headers)

    # Load data into Dictionary and get reading
    data = json.loads(r.text)
    forecast = data['items'][0]['general']['forecast']
    h_ = data['items'][0]['general']['temperature']['high']
    l_ = data['items'][0]['general']['temperature']['low']

    # Create Response
    final_string = "The weather today looks like " + forecast + " with a high of " + str(h_) + \
    "°C and a low of " + str(l_) + "°C"
    bot.sendMessage(update.message.chat_id, text=final_string)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello! I am @ShiokBot! \nThe helpful singlish spouting bot! \n\nAvailable Commands \n/psi - Report the latest PSI readings lo \n/weather - Report the latest weather lah')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello! I am @ShiokBot! \nThe helpful singlish spouting bot! \n\nAvailable Commands \n/psi - Report the latest PSI readings lo \n/weather - Report the latest weather lah')


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
    dp.add_handler(CommandHandler("weather", weathernow))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    """
    #DEV
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    """

    _path = "AAEwNQmrWUDYzDNC9hEmeyRgUPr61ruDqS0"
    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=_path)
    updater.bot.setWebhook("https://shiokbot.herokuapp.com/" + _path)
    updater.idle()

if __name__ == '__main__':
    main()
