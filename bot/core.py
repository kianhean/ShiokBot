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


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

"""Response
weather - Get Latest Weather Report
psi - Get Latest PSI Report
traffic - Get Latest Woodlands or Tuas Traffic Image. Example traffic Tuas
4d - Get Latest 4D Draw Results
ridepromos - Get Latest Promos from Uber/Grab
"""


def fourdresults(bot, update):
    """ Send results from 4D """
    final_string = draw.FourD()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def taxipromos(bot, update):
    """ Get Latest taxipromos """

    text_ = "<b> Latest Uber Promo Codes </b> \n\n"
    text_ += promo.get_code(1)
    text_ += "\n<b> Latest Grab Promo Codes </b> \n\n"
    text_ += promo.get_code(0)

    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')


def traffic(bot, update, args):
    """ Get Traffic Updates """

    if len(args) == 0:
        final_string = 'Please enter either traffic Woodlands or traffic Tuas'
    else:
        final_string = gov.traffic_get(args[0])
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def psi3hour(bot, update):
    """ Get Latest Singapore PSI """

    final_string = gov.psi3hour_get()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def weathernow(bot, update):
    """ Get Latest Singapore Weather """
    final_string = gov.weathernow_get()

    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')


def start(bot, update):
    """ Start Text """
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot! 
                     \nThe helpful singlish spouting bot!
                     \n\nAvailable Commands 
                     \n/psi - Report the latest PSI readings lo
                     \n/weather - Report the latest weather lah
                     \n/4d - Give you latest 4d results wor
                     \n/ridepromos - Help you save money give you uber/grab codes
                     \n/traffic woodlands - Get Latest Woodlands or Tuas Traffic Image. Example traffic Tuas
                     ''')


def help(bot, update):
    """ Help Text"""
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot! 
                     \nThe helpful singlish spouting bot!
                     \n\nAvailable Commands 
                     \n/psi - Report the latest PSI readings lo
                     \n/weather - Report the latest weather lah
                     \n/4d - Give you latest 4d results wor
                     \n/ridepromos - Help you save money give you uber/grab codes
                     \n/traffic woodlands - Get Latest Woodlands or Tuas Traffic Image. Example traffic Tuas
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
    dispatch.add_handler(CommandHandler("ridepromos", taxipromos))
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
