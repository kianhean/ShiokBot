""" Core Bot Functions """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# Import Libraries
import os
import logging
from telegram.ext import Updater, CommandHandler
from bot import gov
from bot import draw
from bot import promo
from bot import finance
from telegram import ReplyKeyboardMarkup, KeyboardButton


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

"""Response
weather - Get Latest Weather Report
psi - Get Latest PSI Report
traffic - Get Latest Traffic Images
4d - Get Latest 4D Draw Results
toto - Get Latest TOTO Draw Results
ridepromos - Get Latest Promos from Uber/Grab
ridepromos_smart - Get Latest Promos from Uber/Grab (Smart List)
sti - Get Latest Straits Times Index Level
sgd - Get Latest SGD FX Rates
sibor - Get Latest SIBOR Rates
"""

"""
REF
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-a-photo-from-a-url
"""

def fourdresults(bot, update):
    """ Send results from 4D """
    final_string = draw.FourD()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def totoresults(bot, update):
    """ Send results from TOTO """
    final_string = draw.TOTO()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def taxipromos(bot, update):
    """ Get Latest taxipromos """

    text_ = "<b>Uber Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(1)
    text_ += "\n<b>Grab Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(0)

    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')


def taxipromos_smart(bot, update):
    """ Get Latest taxipromos Smart """

    text_ = "<b>Smart List of Uber Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(1, smart=True)
    text_ += "\n<b>Smart List of Grab Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(0, smart=True)

    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')


def taxi_around_me(bot, update):
    """ Find Taxis Around me """
    # Detect if in group
    chat_type = update.message.chat.type
    senderid = update.message.from_user.id
    senderusername = update.message.from_user.username

    if chat_type == 'private':
        # Run Code
        send_long = update.message.location.longitude
        send_lat = update.message.location.latitude

        count_ = gov.taxi_get(send_long, send_lat)
        text_ = "There are a total of " + str(count_) + \
        " Available Taxis in a 500M radius Around you!"
        bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    else:
        # Send PM
        message_ = senderusername + \
        ", I sent you a love note. Location can only be shared in private"
        location_keyboard = KeyboardButton(text="/taxi_around_me", request_location=True)
        custom_keyboard = [[location_keyboard]]

        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, selective=True)

        bot.sendMessage(update.message.chat_id, text=message_, parse_mode='HTML')
        bot.sendMessage(senderid, 'Click the button below scan for Available Taxis!',
                        reply_markup=reply_markup)


def traffic(bot, update, args):
    """ Get Traffic Updates """

    if len(args) == 0:
        final_string = 'Please enter either traffic Woodlands or traffic Tuas'
        custom_keyboard = [['/traffic Tuas', '/traffic Woodlands']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, selective=True)
        bot.sendMessage(update.message.chat_id, final_string, reply_markup=reply_markup)

    else:
        final_string = gov.traffic_get(args[0])
        bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def psi3hour(bot, update):
    """ Get Latest Singapore PSI """

    final_string = gov.psi3hour_get()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendPhoto(update.message.chat_id, photo='http://wip.weather.gov.sg/wip/pp/gif/rghz.gif')


def sti_level(bot, update):
    """ Get Latest STI Level """

    final_string = "<b>Straits Times Index Level</b>\nThis is the index today..."
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendPhoto(update.message.chat_id, photo='https://chart.finance.yahoo.com/t?s=%5eSTI&lang=en-SG&region=SG&width=300&height=180')


def sgd_level(bot, update):
    """ Get Latest FX """

    final_string = finance.get_fx()
    final_string += "\nYay can Travel liao!"
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def sibor_level(bot, update):
    """ Get Latest SIBOR """

    final_string = finance.get_sibor()
    final_string += "\nWa Why So High Now!"
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def weathernow(bot, update):
    """ Get Latest Singapore Weather """
    final_string = gov.weathernow_get()

    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendPhoto(update.message.chat_id, photo='http://www.ulfp.com/ulfp/txp_file/download.asp?SRC=download/ulfp/Animate/1_rad70d.gif')


def start(bot, update):
    """ Start Text """
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot!
                     \nThe helpful singlish spouting bot!
                     \nAvailable Commands 
                     \n/psi - Report the latest PSI readings lo
                     \n/weather - Report the latest weather lah
                     \n/4d - Give you latest 4d results wor
                     \n/toto - Give you latest toto results huat ar!
                     \n/ridepromos - Help you save money give you uber/grab codes
                     \n/ridepromos_smart - Help you save money give you uber/grab codes (narrowed down)
                     \n/traffic - Get Latest Traffic Images
                     \n/sti - Get Latest Straits Times Index Level
                     ''')


def help(bot, update):
    """ Help Text"""
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot!
                     \nThe helpful singlish spouting bot!
                     \nAvailable Commands 
                     \n/psi - Report the latest PSI readings lo
                     \n/weather - Report the latest weather lah
                     \n/4d - Give you latest 4d results wor
                     \n/toto - Give you latest toto results huat ar!
                     \n/ridepromos - Help you save money give you uber/grab codes
                     \n/ridepromos_smart - Help you save money give you uber/grab codes (narrowed down)
                     \n/traffic - Get Latest Traffic Images
                     \n/sti - Get Latest Straits Times Index Level
                     ''')


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
    dispatch.add_handler(CommandHandler("toto", totoresults))
    dispatch.add_handler(CommandHandler("ridepromos", taxipromos))
    dispatch.add_handler(CommandHandler("ridepromos_smart", taxipromos_smart))
    dispatch.add_handler(CommandHandler("traffic", traffic, pass_args=True))
    dispatch.add_handler(CommandHandler("sti", sti_level))
    dispatch.add_handler(CommandHandler("sgd", sgd_level))
    dispatch.add_handler(CommandHandler("sibor", sibor_level))
    dispatch.add_handler(CommandHandler("taxi_around_me", taxi_around_me))

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
