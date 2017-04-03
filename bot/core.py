""" Core Bot Functions """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# Import Libraries
import os
import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot import gov
from bot import draw
from bot import promo
from bot import finance
from bot import news
from bot import botan
from telegram import ReplyKeyboardMarkup, KeyboardButton, ChatAction
import emoji


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Enable stats
def botan_track(uid, message, name):
    botan.track(
        token=str(os.environ.get('STATS_API')),
        uid=uid,
        message=message.to_dict(),
        name=name
    )

"""Response
ridepromos - Help you save money give you uber/grab codes
taxi_near_me - Show you the taxis near you!
weather - Report the latest weather lah
sg_news - Latest Headlines from Singapore
traffic - Get Latest Traffic Images
sti - Get Latest Straits Times Index Level
sgd - Latest SGD Rates!      
psi - Report the latest PSI readings lo
4d - Give you latest 4d results wor
toto - Give you latest toto results huat ar!
"""

"""
REF
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-a-photo-from-a-url
"""

def fourdresults(bot, update):
    """ Send results from 4D """
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = draw.FourD()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def totoresults(bot, update):
    """ Send results from TOTO """
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = draw.TOTO()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def taxipromos(bot, update):
    """ Get Latest taxipromos Smart """
    text_bot = ['Let me go and bug Uber/Grab...',
                'Wait ar... I ask my friend Google',
                'Dont you just hate those targeted promos :(',
                'If cannot work not, still friend me ok?',
                'If the discount works remember share share ok',
               ]
    bot.sendMessage(update.message.chat_id, text=random.choice(text_bot),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = "<b>Smart List of Uber Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(1, smart=True)
    text_ += "\n<b>Smart List of Grab Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(0, smart=True)
    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def taxi_around_me(bot, update):
    """ Find Taxis Around me """
    # Detect if in group
    chat_type = update.message.chat.type
    senderid = update.message.from_user.id
    senderusername = update.message.from_user.username

    text_bot = ['I go see see look look...',
                'Get ready to run...',
                'I find where they hiding now...',
                'Usually if i want to go somewhere i let my fingers do the walking'
               ]

    if chat_type == 'private':

        success_status = False

        # Run Code
        try:
            # If already sent the message
            send_long = update.message.location.longitude
            send_lat = update.message.location.latitude
            success_status = True
        except:
            # If have not sent the message
            location_keyboard = KeyboardButton(text="/taxi_around_me", request_location=True)
            custom_keyboard = [[location_keyboard]]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True,
                                               selective=True)
            bot.sendMessage(senderid, 'Click the button below scan for Available Taxis!',
                            reply_markup=reply_markup)

        if success_status:
            bot.sendMessage(update.message.chat_id, text=random.choice(text_bot),
                            parse_mode='HTML')
            bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)

            taxi = gov.taxi_get(send_long, send_lat)
            text_ = "There are a total of " + str(taxi['count_number']) + \
            " Available Taxis (not uber/grab) in a 200M radius Around you!"
            bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')

            if taxi['count_number'] > 0:
                bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
                bot.sendPhoto(update.message.chat_id, photo=taxi['url'])
                bot.sendMessage(update.message.chat_id, text='Run my child, run...',
                                parse_mode='HTML')
            else:
                bot.sendMessage(update.message.chat_id, text='No taxi!?! Why u at ulu place?',
                                parse_mode='HTML')
            botan_track(update.message.from_user.id, update.message, update.message.text)

    else:
        # If in group chat... send PM
        location_keyboard = KeyboardButton(text="/taxi_around_me", request_location=True)
        custom_keyboard = [[location_keyboard]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, selective=True)
        pm_try = False

        try:
            # Try to send PM, will have an error if never added before
            bot.sendMessage(senderid, 'Click the button below scan for Available Taxis!',
                            reply_markup=reply_markup)
            pm_try = True
        except:
            message_ = "You have to start a convo with me first! @ShiokBot before I can send you this info!"
            bot.sendMessage(update.message.chat_id, text=message_, parse_mode='HTML')
            message_ = "After starting the PM with me try /taxi_around_me again"
            bot.sendMessage(update.message.chat_id, text=message_, parse_mode='HTML')

        if pm_try:
            message_ = senderusername + \
            ", I sent you a love note. Location can only be shared in private"
            bot.sendMessage(update.message.chat_id, text=message_, parse_mode='HTML')

def traffic(bot, update, args):
    """ Get Traffic Updates """

    if len(args) == 0:
        final_string = 'Please enter either traffic Woodlands or traffic Tuas'
        custom_keyboard = [['/traffic Tuas', '/traffic Woodlands']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, selective=True)
        bot.sendMessage(update.message.chat_id, final_string, reply_markup=reply_markup)

    else:
        bot.sendMessage(update.message.chat_id, text='I go turn on my spycam, please wait',
                        parse_mode='HTML')
        bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
        final_string = gov.traffic_get(args[0])
        bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
        botan_track(update.message.from_user.id, update.message, update.message.text)


def psi3hour(bot, update):
    """ Get Latest Singapore PSI """
    text_bot = ['Putting my hand in the air to feel the dust...',
                'Sometimes I wear my N95 mask as a fashion statement',
                'Unlike you, i am not affected by Haze',
                'Air quality in the cloud, is the freshest...'
               ]
    bot.sendMessage(update.message.chat_id, text=random.choice(text_bot),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = gov.psi3hour_get()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendPhoto(update.message.chat_id, photo='http://wip.weather.gov.sg/wip/pp/gif/rghz.gif')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def get_news_st(bot, update):
    """ Get Latest Singapore PSI """
    bot.sendMessage(update.message.chat_id, text='Reading the Newspapers...',
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = news.get_news_st()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML', disable_web_page_preview=True)
    botan_track(update.message.from_user.id, update.message, update.message.text)


def sti_level(bot, update):
    """ Get Latest STI Level """

    final_string = "<b>Straits Times Index Level</b>\nThis is the index today..."
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    bot.sendPhoto(update.message.chat_id, photo='https://chart.finance.yahoo.com/t?s=%5eSTI&lang=en-SG&region=SG&width=300&height=180')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def sgd_level(bot, update):
    """ Get Latest FX """
    bot.sendMessage(update.message.chat_id, text='Let me go arcade and spy...',
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = finance.get_fx()
    final_string += "\nYay can Travel liao!"
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def sibor_level(bot, update):
    """ Get Latest SIBOR """
    bot.sendMessage(update.message.chat_id, text='Let me ask the GAHMEN...',
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = finance.get_sibor()
    final_string += "\nWa Why So High Now!"
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def weathernow(bot, update):
    """ Get Latest Singapore Weather """
    text_bot = ['Let me look out of the window...',
                'Why dont you look out of the window instead?',
                'Dont cry for me roti prataaaaa...',
                'If there is a flood remember that fat people dont actually float...'
               ]
    bot.sendMessage(update.message.chat_id, text=random.choice(text_bot),
                    parse_mode='HTML')
    final_string = gov.weathernow_get()

    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    bot.sendPhoto(update.message.chat_id,
                  photo='http://www.ulfp.com/ulfp/txp_file/download.asp?SRC=download/ulfp/Animate/1_rad70d.gif')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def start(bot, update):
    """ Start Text """
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot!
                     \nThe helpful singlish spouting bot!
                     \nAvailable Commands
                     \n/weather - Report the latest weather lah
                     \n/sg_news - Latest Headlines from Singapore

                     \n/ridepromos - Help you save money give you uber/grab codes
                     \n/taxi_near_me - Show you the taxis near you!
                     \n/traffic - Get Latest Traffic Images
                     \n/sti - Get Latest Straits Times Index Level
                     \n/sgd - Latest SGD Rates!
                    
                     \n/psi - Report the latest PSI readings lo
                     \n/4d - Give you latest 4d results wor
                     \n/toto - Give you latest toto results huat ar!
                     ''')


def help(bot, update):
    """ Help Text"""
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot!
                     \nThe helpful singlish spouting bot!
                     \nAvailable Commands
                     \n/weather - Report the latest weather lah
                     \n/sg_news - Latest Headlines from Singapore

                     \n/ridepromos - Help you save money give you uber/grab codes
                     \n/taxi_near_me - Show you the taxis near you!
                     \n/traffic - Get Latest Traffic Images
                     \n/sti - Get Latest Straits Times Index Level
                     \n/sgd - Latest SGD Rates!
                    
                     \n/psi - Report the latest PSI readings lo
                     \n/4d - Give you latest 4d results wor
                     \n/toto - Give you latest toto results huat ar!
                     ''')


def error(bot, update, error):
    """ Log Errors"""
    logger.warning('Update "%s" caused error "%s"' % (update, error))


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
    dispatch.add_handler(CommandHandler("sg_news", get_news_st))
    dispatch.add_handler(CommandHandler("traffic", traffic, pass_args=True))
    dispatch.add_handler(CommandHandler("sti", sti_level))
    dispatch.add_handler(CommandHandler("sgd", sgd_level))
    dispatch.add_handler(CommandHandler("sibor", sibor_level))
    dispatch.add_handler(CommandHandler("taxi_near_me", taxi_around_me))
    dispatch.add_handler(MessageHandler([Filters.location], taxi_around_me))

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
