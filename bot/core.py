""" Core Bot Functions """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# Import Libraries
import os
import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, CallbackQueryHandler
from bot import gov
from bot import draw
from bot import promo
from bot import finance
from bot import news
from bot import botan
from bot import promo_alert
from bot import train_alert
from bot import promo_general
from telegram import ReplyKeyboardMarkup, KeyboardButton, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize # emojize(random.choice(text_bot), use_aliases=True)
from functools import wraps
from time import sleep
import datetime


LIST_OF_ADMINS = [22959774]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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
ridepromos - Help you save money give you grab/comfort codes
train_timing_changes - Updates to MRT timing due to mantainance works
deliverypromos - Help you save money with uber/deliveroo/honestbee/foodpanda codes
airlinepromos - Help you save money with airline codes
hotelpromos - Help you save money with hotel codes
shoppingpromos - Help you save money with Online Shopping codes
share - Easily Share Shiokbot with Friends!
subscribe - Subscribe to Uber Promo Alerts
subscribe_train - Subscribe to Train breakdown Alerts
sg_news - Latest Headlines from Singapore
sgd - Latest SGD Rates!
weather - Report the latest weather lah
psi - Report the latest PSI readings lo
4d - Give you latest 4d results wor
toto - Give you latest toto results huat ar!
traffic - Get Latest Traffic Images
taxi_near_me - Show you taxis near you!
sibor - Latest Sibor Rates!
unsubscribe - Unsubscribe to Uber Promo Alerts :(
unsubscribe_train - Unsubscribe to Train breakdown Alerts :(
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


def taxipromos2(bot, update):
    """ Get Latest taxipromos Smart """
    text_bot = ['Let me go and bug Grab :sunglasses:',
                'Wait ar... I ask my friend Google :wink: :wink:',
                'Dont you just hate those targeted promos :weary:',
                'If cannot work, still friend me ok? :stuck_out_tongue:',
                'If the discount works remember share share ok :smirk:',
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = "<b>:large_blue_circle:List of ComfortDelgro Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(1, smart=True)
    text_ += "\n<b>:white_check_mark:List of Grab Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code(0, smart=True)

    # Update Feature with Inline Keyboard
    promo_keyboard = InlineKeyboardButton(text="Update!", callback_data="update_taxi")
    custom_keyboard = [[promo_keyboard]]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)

    bot.sendMessage(update.message.chat_id, text=emojize(text_, use_aliases=True),
                    parse_mode='HTML', reply_markup=reply_markup)
    botan_track(update.message.from_user.id, update.message, update.message.text)

    ad_msg = "Click on /subscribe@shiokbot to subscribe to Uber Promo Codes! Be notified instantly!\n"
    ad_msg += "Click on /subscribe_train@shiokbot to subscribe to Train Breakdown Alerts! Preview : https://goo.gl/1UrmL6"

    bot.sendMessage(update.message.chat_id,
                    ad_msg, disable_web_page_preview=True,
                    parse_mode='HTML')


def call_handler(bot, update):
    """ https://stackoverflow.com/questions/39121678/updating-messages-with-inline-keyboards-using-callback-queries """

    if update.callback_query.data == 'update_taxi':
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                text="Refreshing Promo Codes...")

        text_ = "<b>:black_large_square:List of Uber Promo Codes (Latest on Top)</b> \n\n"
        text_ += promo.get_code(1, smart=True)
        text_ += "\n<b>:white_check_mark:List of Grab Promo Codes (Latest on Top)</b> \n\n"
        text_ += promo.get_code(0, smart=True)
        text_ += "\n :repeat:Last Update: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update Feature with Inline Keyboard
        promo_keyboard = InlineKeyboardButton(text="Update!", callback_data="update_taxi")
        custom_keyboard = [[promo_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)

        bot.editMessageText(
            message_id=update.callback_query.message.message_id,
            chat_id=update.callback_query.message.chat.id,
            text=emojize(text_, use_aliases=True),
            parse_mode='HTML',
            reply_markup=reply_markup
        )

def train_timing_changes(bot, update):
    """ Get Latest taxipromos Smart """
    text_bot = ['Checking for Train Schedule Changes :sunglasses:',
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = "<b>:train2:Changes to train service hours</b> \n\n"
    text_ += train_alert.train_operating_changes()
    bot.sendMessage(update.message.chat_id, text=emojize(text_, use_aliases=True),
                    parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def deliverypromos(bot, update):
    """ Get Latest taxipromos Smart """
    text_bot = ['Let me go and bug Uber/Deliveroo :sunglasses:',
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = "<b>:black_large_square:List of UberEats Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code_normal('https://www.cheapcheaplah.com/deals/ubereats.com')
    text_ += "\n<b>:four_leaf_clover:List of Deliveroo Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code_normal('https://www.cheapcheaplah.com/deals/deliveroo.com.sg')
    text_ += "\n<b>:honeybee:List of HonestBee Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code_normal('https://www.cheapcheaplah.com/deals/honestbee.sg')
    text_ += "\n<b>:panda_face:List of FoodPanda Promo Codes (Latest on Top)</b> \n\n"
    text_ += promo.get_code_normal('https://www.cheapcheaplah.com/deals/foodpanda.sg')
    bot.sendMessage(update.message.chat_id, text=emojize(text_, use_aliases=True),
                    parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def airline_promos(bot, update):
    """ Get Latest Airline Promos """
    promo_list = {'Scoot':'https://www.couponese.com/store/flyscoot.com/',
                  'Tigerair':'https://www.couponese.com/store/tigerair.com/',
                  'AirAsia':'https://www.couponese.com/store/airasia.com/',
                  'Singaporeair':'https://www.couponese.com/store/singaporeair.com/',
                  'CheapTickers':'https://www.couponese.com/store/cheaptickets.sg/'
                 }
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = promo_general.promo_loop(promo_list)
    text_ = ":airplane::airplane::airplane:" + text_
    bot.sendMessage(update.message.chat_id, text=emojize(text_, use_aliases=True),
                    parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)

def hotel_promos(bot, update):
    """ Get Latest Hotel Promos """
    promo_list = {'Zuji':'https://www.couponese.com/store/zuji.com.sg/',
                  'Hotels.com':'https://www.couponese.com/store/hotels.com/',
                  'Expedia':'https://www.couponese.com/store/expedia.com.sg/'
                 }
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = promo_general.promo_loop(promo_list)
    text_ = ":office::office::office:" + text_
    bot.sendMessage(update.message.chat_id, text=emojize(text_, use_aliases=True),
                    parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)

def shopping_promos(bot, update):
    """ Get Latest Shopping Promos """
    promo_list = {'Lazada':'https://www.couponese.com/store/lazada.sg/',
                  'Amazon':'https://www.couponese.com/store/amazon.com.sg/',
                  'Redmart':'https://www.couponese.com/store/redmart.com/',
                  'Zalora':'https://www.couponese.com/store/zalora.sg/',
                 }
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    text_ = promo_general.promo_loop(promo_list)
    text_ = ":handbag::handbag::handbag:" + text_
    bot.sendMessage(update.message.chat_id, text=emojize(text_, use_aliases=True),
                    parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def subscribe(bot, update):
    """ Subscribe Latest taxipromos Smart """
    text_ = promo_alert.subscribe(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def unsubscribe(bot, update):
    """ Unsub Latest taxipromos Smart """
    text_ = promo_alert.unsubscribe(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def subscribe_train(bot, update):
    """ Subscribe Latest train alerts """
    text_ = train_alert.subscribe(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def unsubscribe_train(bot, update):
    """ Unsub Latest train alerts """
    text_ = train_alert.unsubscribe(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def secret_sauce(bot, update):
    text_ = "Secret HDL Sauce!"
    bot.sendMessage(update.message.chat_id, text=text_, parse_mode='HTML')
    bot.sendPhoto(update.message.chat_id,
                  photo="https://user-images.githubusercontent.com/5037305/27761010-dbdb1560-5e86-11e7-90b8-38a4e0274d17.jpg")


def monitor_train(bot, job):
    """ Job to Send Train Message """
    msg = train_alert.get_new_breakdowns_message()

    if msg is None:
        print('No new breakdowns')
    else:
        all_users = train_alert.get_all_users()
        to_send = chunks(all_users, 10)

        for group in to_send:
            for user in group:
                try:
                    bot.sendMessage(int(user), text=emojize(msg, use_aliases=True),
                                    parse_mode='HTML')
                except:
                    print("Error! Sending Message to " + str(user))
            sleep(1.2)


def monitor_promo(bot, job):
    """ Job to Send Promo Message """
    msg = promo_alert.get_new_codes_message()

    if msg is None:
        print('No new promos')
    else:
        text_bot = ['Uber poked me privately and said this :wink:',
                    'I found this promo code while I was in my ActiveWear! :stuck_out_tongue:',
                    'Quick apply the code! Later run out dont cry :sunglasses:',
                    'Breaking News Brought to you by ShiokBot!',
                   ]
        all_users = promo_alert.get_all_users()
        to_send = chunks(all_users, 10)

        for group in to_send:
            for user in group:
                try:
                    bot.sendMessage(int(user),
                                    text=emojize(random.choice(text_bot), use_aliases=True),
                                    parse_mode='HTML')
                    bot.sendMessage(int(user), text=msg, parse_mode='HTML')
                except:
                    print("Error! Sending Message to " + str(user))
            sleep(1.2)


@restricted
def clear_db(bot, update):
    train_alert.clear_db()
    bot.sendMessage(22959774, text='Train Database Cleared!', parse_mode='HTML')


@restricted
def list_users(bot, update):
    userlist = promo_alert.get_all_users()
    msg = str(len(userlist)) + ' Users Subscribed To Promo Alerts!'

    bot.sendMessage(22959774, text=msg, parse_mode='HTML')


@restricted
def push_notification_promo(bot, update, args):
    """
    Send Promo Push Notification!
    Example
    <b>SHIOKBOT3</b> | Expires - 02/11/2017 | $3 off uberX and uberPOOL
    """
    text_bot = ['An Exclusive Promotion For ShiokBot Users Only! :wink:',
                ]

    # Compile Sending List
    all_users = promo_alert.get_all_users()
    #all_users = [22959774]
    to_send = chunks(all_users, 10)

    # Compile Words
    text_promo = ''
    for word in args:
        text_promo += word + " "

    for group in to_send:
        for user in group:
            try:
                bot.sendMessage(int(user),
                                text=emojize(random.choice(text_bot), use_aliases=True),
                                parse_mode='HTML')
                bot.sendMessage(int(user), text=text_promo, parse_mode='HTML')
            except:
                print("Error! Sending Message to " + str(user))
        sleep(1.2)

@restricted
def push_notification_msg(bot, update, args):
    """
    Send Service Notification
    Example
    <b>Service Notification</b> \n\n Apologies for the downtime earlier!
    """

    # Compile Sending List
    #all_users = promo_alert.get_all_users()
    #all_users.append(train_alert.get_all_users())
    #all_users = list(set(all_users))

    all_users = [22959774]
    all_users.append([22959774])
    all_users = list(set(all_users))

    to_send = chunks(all_users, 10)

    # Compile Words
    text_promo = ''
    for word in args:
        text_promo += word + " "

    for group in to_send:
        for user in group:
            try:
                bot.sendMessage(int(user), text=text_promo, parse_mode='HTML')
            except:
                print("Error! Sending Message to " + str(user))
        sleep(1.2)


@restricted
def list_users_train(bot, update):
    userlist = train_alert.get_all_users()
    msg = str(len(userlist)) + ' Users Subscribed To Train Alerts!'

    bot.sendMessage(22959774, text=msg, parse_mode='HTML')


@restricted
def force_promo_check(bot, update):
    """ Job to Send Message """
    msg = promo_alert.get_new_codes_message()

    if msg is None:
        bot.sendMessage(22959774, text="No new Promos", parse_mode='HTML')
    else:
        bot.sendMessage(22959774, text=msg, parse_mode='HTML')

    bot.sendMessage(22959774, text='Forced Promo Check!', parse_mode='HTML')


def taxi_around_me(bot, update):
    """ Find Taxis Around me """
    # Detect if in group
    chat_type = update.message.chat.type
    senderid = update.message.from_user.id
    senderusername = update.message.from_user.username

    text_bot = ['I go see see look look... :eyes:',
                'Get ready to run :running:',
                'I find where they hiding now :eyes: :eyes:',
                'Usually if i want to go somewhere i let my fingers do the walking :v:'
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
            location_keyboard = KeyboardButton(text="/taxi_near_me", request_location=True)
            custom_keyboard = [[location_keyboard]]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True,
                                               selective=True)
            bot.sendMessage(senderid, 'Click the button below scan for Available Taxis!',
                            reply_markup=reply_markup)

        if success_status:
            bot.sendMessage(update.message.chat_id,
                            text=emojize(random.choice(text_bot), use_aliases=True),
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
        location_keyboard = KeyboardButton(text="/taxi_near_me", request_location=True)
        custom_keyboard = [[location_keyboard]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, selective=True)
        pm_try = False

        try:
            # Try to send PM, will have an error if never added before
            bot.sendMessage(senderid, 'Click the button below scan for Available Taxis!',
                            reply_markup=reply_markup)
            pm_try = True
        except:

            # Promo Feature with Inline Keyboard
            promo_keyboard = InlineKeyboardButton(text="PM Me!",
                                                  url="https://telegram.me/shiokbot?start")
            custom_keyboard = [[promo_keyboard]]
            reply_markup = InlineKeyboardMarkup(custom_keyboard)

            message_ = "You have to start a convo with me first! @ShiokBot before I can send you this info!\n\nAfter starting the PM with me try /taxi_near_me again"
            bot.sendMessage(update.message.chat_id, text=message_,
                            parse_mode='HTML', reply_markup=reply_markup)

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
    text_bot = ['Putting my hand in the air to feel the dust :point_up:',
                'Sometimes I wear my N95 mask as a fashion statement :sunglasses:',
                'Unlike you, i am not affected by Haze :alien:',
                'Air smells the freshes when hosted in the :cloud:'
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = gov.psi3hour_get()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendPhoto(update.message.chat_id, photo='http://wip.weather.gov.sg/wip/pp/gif/rghz.gif')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def get_news_st(bot, update):
    """ Get Latest Singapore News """
    text_bot = ['Fake news is only fake because you are real :smiling_imp:',
                'Let me tell you a story!',
                'You read, I parse :smirk:'
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
                    parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    final_string = news.get_news_st()
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML',
                    disable_web_page_preview=True)
    botan_track(update.message.from_user.id, update.message, update.message.text)


def sti_level(bot, update):
    """ Get Latest STI Level """
    final_string = "<b>Straits Times Index Level</b>\nThis is the index today..."
    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    bot.sendPhoto(update.message.chat_id,
                  photo='https://chart.finance.yahoo.com/t?s=%5eSTI&lang=en-SG&region=SG&width=300&height=180')
    botan_track(update.message.from_user.id, update.message, update.message.text)


def sgd_level(bot, update):
    """ Get Latest FX """
    text_bot = ['The markets may be bad, but i slept like baby, every hour i woke up and cry. :smiling_imp:',
                'The one with the shortest queue is the best :scream:',
                'If only everyone displays FX rates as clearly as me :smirk:',
                'Bots usually use Bitcoin, dealing with humans is boringgg'
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
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
    text_bot = ['Let me look out of the window... :dash:',
                'Why dont you look out of the window instead? :smirk:',
                'Dont cry for me roti prataaaaa... :scream:',
                'How do meteorologists say hi? With a heat wave! hahahaha'
               ]
    bot.sendMessage(update.message.chat_id, text=emojize(random.choice(text_bot), use_aliases=True),
                    parse_mode='HTML')
    final_string = gov.weathernow_get()
    warning = gov.weather_warning_get()

    if warning != "No Warnings!":
        bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
        bot.sendMessage(update.message.chat_id, text=warning, parse_mode='HTML')

    bot.sendMessage(update.message.chat_id, text=final_string, parse_mode='HTML')
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    bot.sendPhoto(update.message.chat_id, photo=gov.get_latestmap_website())
    botan_track(update.message.from_user.id, update.message, update.message.text)


def start(bot, update):
    """ Start Text """
    bot.sendMessage(update.message.chat_id,
                    text='''Hello! I am @ShiokBot!
                     \nThe helpful singlish spouting bot!
                     \nAvailable Commands

                     \n/ridepromos - Help you save money give you Uber/grab codes
                     \n/subscribe - Subscribe to the latest Uber codes as they come out!
                     \n/subscribe_train - Subscribe to Train breakdown Alerts
                     \n/share - Easily Share Shiokbot!

                     \n/weather - Report the latest weather lah
                     \n/sg_news - Latest Headlines from Singapore

                     \n/taxi_near_me - Show you the taxis near you!
                     \n/traffic - Get Latest Traffic Images
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

                     \n/ridepromos - Help you save money give you Uber/grab codes
                     \n/subscribe - Subscribe to the latest Uber codes as they come out!
                     \n/subscribe_train - Subscribe to Train breakdown Alerts
                     \n/share - Easily Share Shiokbot!

                     \n/weather - Report the latest weather lah
                     \n/sg_news - Latest Headlines from Singapore

                     \n/taxi_near_me - Show you the taxis near you!
                     \n/traffic - Get Latest Traffic Images
                     \n/sgd - Latest SGD Rates!
                    
                     \n/psi - Report the latest PSI readings lo
                     \n/4d - Give you latest 4d results wor
                     \n/toto - Give you latest toto results huat ar!
                     ''')


def share(bot, update):
    """ Share Text"""

    version_text = """
                    Version Log
                    \n\n <b>Version 3.5 - 13 May 2018</b>
                    \n Remove Uber, Add more Delivery Providers
                    \n Added Train Schedule Changes
                    \n\n <b>Version 3.4 - 30 Jul 2017</b>
                    \n Online Shopping Promos
                    \n\n <b>Version 3.3 - 28 Jun 2017</b>
                    \n Added Share cmd
                    \n Launch Train Breakdown Notifications
                    \n <b>Version 3.2 - 26 Jun 2017</b>
                    \n Testing Train breakdown Notification
                    \n Fixed promo monitor bugs
                    \n b>Version 3.1 - 22 Jun 2017</b>
                    \n Wa kenna featured on TSL
                    \n Removed STI Yahoo API is gone"""
    share_text = """
                 Shiokbot thanks you for sharing the love\n
                 Send this link to your friends to start using!\n
                 <b>https://t.me/shiokbot?start</b>
                 \nMore Information Here!
                 \nhttps://kianhean.com/2016/12/20/singapore-telegram-bot/
                 """
    bot.sendMessage(update.message.chat_id,
                    text=share_text, parse_mode='HTML')
    #bot.sendMessage(update.message.chat_id,
    #                text=version_text, parse_mode='HTML')


def error(bot, update, error):
    """ Log Errors"""
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    """ This is where the bot starts from! """

    # Create the EventHandler and pass it your bot's token.
    telegram = str(os.environ.get('TELEGRAM'))
    updater = Updater(telegram)
    j = updater.job_queue

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(CommandHandler("start", start))
    dispatch.add_handler(CommandHandler("help", help))
    dispatch.add_handler(CommandHandler("psi", psi3hour))
    dispatch.add_handler(CommandHandler("weather", weathernow))
    dispatch.add_handler(CommandHandler("4d", fourdresults))
    dispatch.add_handler(CommandHandler("toto", totoresults))
    dispatch.add_handler(CommandHandler("ridepromos", taxipromos2))
    dispatch.add_handler(CommandHandler("airlinepromos", airline_promos))
    dispatch.add_handler(CommandHandler("deliverypromos", deliverypromos))
    dispatch.add_handler(CommandHandler("shoppingpromos", shopping_promos))
    dispatch.add_handler(CommandHandler("train_timing_changes", train_timing_changes))
    dispatch.add_handler(CommandHandler("sg_news", get_news_st))
    dispatch.add_handler(CommandHandler("traffic", traffic, pass_args=True))
    # dispatch.add_handler(CommandHandler("sti", sti_level))
    dispatch.add_handler(CommandHandler("sgd", sgd_level))
    dispatch.add_handler(CommandHandler("hotel_promos", hotel_promos))
    dispatch.add_handler(CommandHandler("sibor", sibor_level))
    dispatch.add_handler(CommandHandler("taxi_near_me", taxi_around_me))
    dispatch.add_handler(CommandHandler("subscribe", subscribe))
    dispatch.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dispatch.add_handler(CommandHandler("subscribe_train", subscribe_train))
    dispatch.add_handler(CommandHandler("unsubscribe_train", unsubscribe_train))
    dispatch.add_handler(CommandHandler("admin_force_promo_check", force_promo_check))
    dispatch.add_handler(CommandHandler("admin_clear_db", clear_db))
    dispatch.add_handler(CommandHandler("admin_list_users", list_users))
    dispatch.add_handler(CommandHandler("admin_push_notification_promo", push_notification_promo, pass_args=True))
    dispatch.add_handler(CommandHandler("admin_push_notification_msg", push_notification_msg, pass_args=True))
    dispatch.add_handler(CommandHandler("share", share))
    dispatch.add_handler(CommandHandler("secret_sauce", secret_sauce))
    dispatch.add_handler(CommandHandler("admin_list_users_train", list_users_train))
    dispatch.add_handler(MessageHandler(Filters.location, taxi_around_me))
    dispatch.add_handler(CallbackQueryHandler(call_handler))

    # create jobs
    # job_minute = Job(monitor_promo, 900)
    # j.put(job_minute, next_t=60)

    # Uber Discontinued
    #j.run_repeating(monitor_promo, 600, 15)
    j.run_repeating(monitor_train, 300, 60)

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
