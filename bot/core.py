""" Core Bot Functions """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# Import Libraries
import os
import logging
import json
import requests
from telegram.ext import Updater, CommandHandler
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

"""Response
weather - Get Latest Weather Report
psi - Get Latest PSI Report
traffic - Get Latest Woodlands or Tuas Traffic Image. Example traffic Tuas
"""


def connnect_gov_api(url_string):
    """ Conntect to Gov and return request object """
    data_gov_api = str(os.environ.get('DATAGOV'))
    headers = {'api-key': data_gov_api}
    request = requests.get(url_string, headers=headers)

    return request


def FourD():
    """4D Methods!"""

    # Connect to Source
    url = 'https://www.gidapp.com/lottery/singapore/4d'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    result = soup.findAll('time')
    latest_result_date = result[6].get_text()

    result = soup.find_all('span')

    # TOP PRIZES
    first = result[8].get_text()
    second = result[9].get_text()
    third = result[10].get_text()

    top_text = "1st - " + first + "\n2nd - " + second + "\n3rd - " + third + "\n\n"

    # SPECIAL PRIZE
    special_prize = "Special/Starter Prizes\n\n"
    for i in range(11, 21):
        special_prize +=  result[i].get_text() + "  "

    # CONSOLATION PRIZE
    consol_prize = "\n\nConsolation Prizes\n\n"
    for i in range(21, 31):
        consol_prize +=  result[i].get_text() + "  "

    # Create Reply
    chat_reply = "Latest Draw Results on " + latest_result_date + " \n\n"
    chat_reply += top_text
    chat_reply += special_prize
    chat_reply += consol_prize
    chat_reply += "\n\n No need check la sure never win!"

    return chat_reply


def fourdresults(bot, update):
    """ Send results from 4D """
    final_string = FourD()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def traffic(bot, update, args):
    """ Get Traffic Updates """

    connnect_gov_api_r = connnect_gov_api('https://api.data.gov.sg/v1/transport/traffic-images')
    data = json.loads(connnect_gov_api_r.text)

    if len(args) == 0:
        final_string = 'Please enter either traffic Woodlands or traffic Tuas'
        bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
        return
    else:
        location = str(args[0]).upper()

    if location == 'TUAS':
        target_ = '4703' # Tuas
    elif location == 'WOODLANDS':
        target_ = '2701' # Woodlands
    else:
        final_string = 'Sorry for now only understooded either Tuas or Woodlands!'
        bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
        return

    # Get required data
    for data_ in data['items'][0]['cameras']:
        if (data_['camera_id']) == target_:
            img_url = data_['image']
            timestampp = data_['timestamp'][:19].replace("T", " ")

    # Create Response
    final_string = "The " + location.title() + " Checkpoint Situation at " + \
                   timestampp + " is like that la \n\n"

    final_string = final_string + '<a href="' +img_url+ '">Traffic Image!</a>'
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def psi3hour(bot, update):
    """ Get Latest Singapore PSI """

    connnect_gov_api_r = connnect_gov_api('https://api.data.gov.sg/v1/environment/psi')
    data = json.loads(connnect_gov_api_r.text)

    # Load data into Dictionary and get reading
    hourly = data['items'][0]['readings']['psi_three_hourly']
    timestampp = data['items'][0]['timestamp'][:19].replace("T", " ")

    # Create Response
    final_string = "The 3 hourly PSI Reading at " + timestampp + " is actually \n\n"
    for key in sorted(hourly):
        final_string  =  final_string + (str(key) + " " + \
                                        str(hourly[key]) + "\n")
    bot.sendMessage(update.message.chat_id, text=final_string)


def weathernow(bot, update):
    """ Get Latest Singapore Weather """
    connnect_gov_api_r = connnect_gov_api(
        'https://api.data.gov.sg/v1/environment/24-hour-weather-forecast')
    data = json.loads(connnect_gov_api_r.text)

    # Load data into Dictionary and get reading
    forecast = data['items'][0]['general']['forecast']
    high_ = data['items'][0]['general']['temperature']['high']
    low_ = data['items'][0]['general']['temperature']['low']

    # Create Response
    final_string = "In General the weather will be looking like " + forecast + \
                    " with a high of " + str(high_) + \
                    "°C and a low of " + str(low_) + "°C\n\nForecast Next 12 Hrs\n\n"

    # Add 12 hr cast
    nowcast = data['items'][0]['periods'][0]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + \
                                        " - " + str(nowcast[key]) + "\n")
    final_string = final_string + "\nForecast Tomorrow\n\n"

    # Add 24 hr cast
    nowcast = data['items'][0]['periods'][1]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + " - " + str(nowcast[key]) + "\n")

    bot.sendMessage(update.message.chat_id, text=final_string)


def start(bot, update):
    """ Start Text """
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot! \nThe helpful singlish spouting bot!
                     \n\nAvailable Commands \n/psi - Report the latest PSI readings lo
                      \n/weather - Report the latest weather lah''')


def help(bot, update):
    """ Help Text"""
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot! \nThe helpful singlish spouting bot!
                         \n\nAvailable Commands \n/psi - 
                         Report the latest PSI readings lo \n/weather -
                          Report the latest weather lah''')


def error(bot, update, error):
    """ Log Errors"""
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    """ This is where the bot starts from! """

    # Create the EventHandler and pass it your bot's token.
    telegram = str(os.environ.get('TELEGRAM'))
    updater = Updater(telegram)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(CommandHandler("start", start))
    dispatch.add_handler(CommandHandler("help", help))
    dispatch.add_handler(CommandHandler("psi", psi3hour))
    dispatch.add_handler(CommandHandler("weather", weathernow))
    dispatch.add_handler(CommandHandler("4d", fourdresults))
    dispatch.add_handler(CommandHandler("traffic", traffic, pass_args=True))

    # log all errors
    dispatch.add_error_handler(error)

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
    port_number = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                          port=port_number,
                          url_path=telegram)
    updater.bot.setWebhook("https://shiokbot.herokuapp.com/" + telegram)
    updater.idle()

if __name__ == '__main__':
    main()
