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

"""Response
weather - Get Latest Weather Report
psi - Get Latest PSI Report
traffic_tuas - Get Latest Tuas Traffic Image
"""


def traffic_tuas(bot, update):

    # Make the HTTP request.
    DATAGOV = str(os.environ.get('DATAGOV'))
    headers = {'api-key': DATAGOV}
    r = requests.get('https://api.data.gov.sg/v1/transport/traffic-images', headers=headers)

    # Load data into Dictionary and get reading
    data = json.loads(r.text)
    target_ = '4703' # Tuas
    #target_ = '2701' # Woodlands

    # Get required data
    for data_ in data['items'][0]['cameras']:
        if (data_['camera_id']) == target_: # Woodlands
            img_url = data_['image']
            timestampp = data_['timestamp'][:19].replace("T"," ")

    # Create Response
    final_string = "The Tuas Checkpoint Situation at " + timestampp + " is like that la \n\n"
    final_string = final_string + '<a href="' +img_url+ '">Traffic Image!</a>'
    #bot.sendPhoto(update.message.chat_id, caption=final_string, photo=img_url)
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def psi3hour(bot, update):

    # Make the HTTP request.
    DATAGOV = str(os.environ.get('DATAGOV'))
    headers = {'api-key': DATAGOV}
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
    DATAGOV = str(os.environ.get('DATAGOV'))
    headers = {'api-key': DATAGOV}
    r = requests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast', headers=headers)

    # Load data into Dictionary and get reading
    data = json.loads(r.text)
    forecast = data['items'][0]['general']['forecast']
    h_ = data['items'][0]['general']['temperature']['high']
    l_ = data['items'][0]['general']['temperature']['low']

    # Create Response
    final_string = "In General the weather will be looking like " + forecast + " with a high of " + str(h_) + \
    "°C and a low of " + str(l_) + "°C\n\nForecast Next 12 Hrs\n\n"

    # Add 12 hr cast
    nowcast = data['items'][0]['periods'][0]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + " - " + str(nowcast[key]) + "\n")
    final_string = final_string + "\nForecast Tomorrow\n\n"

    # Add 24 hr cast
    nowcast = data['items'][0]['periods'][1]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + " - " + str(nowcast[key]) + "\n")

    bot.sendMessage(update.message.chat_id, text=final_string)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello! I am @ShiokBot! \nThe helpful singlish spouting bot! \n\nAvailable Commands \n/psi - Report the latest PSI readings lo \n/weather - Report the latest weather lah')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello! I am @ShiokBot! \nThe helpful singlish spouting bot! \n\nAvailable Commands \n/psi - Report the latest PSI readings lo \n/weather - Report the latest weather lah')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    TELEGRAM = str(os.environ.get('TELEGRAM'))
    updater = Updater(TELEGRAM)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("psi", psi3hour))
    dp.add_handler(CommandHandler("weather", weathernow))
    dp.add_handler(CommandHandler("traffic_tuas", traffic_tuas))

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

    #PROD
    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TELEGRAM)
    updater.bot.setWebhook("https://shiokbot.herokuapp.com/" + TELEGRAM)
    updater.idle()

if __name__ == '__main__':
    main()
