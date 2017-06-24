import tweepy
from datetime import datetime, timedelta
import dataset
import os

# Set Keys
database_url = str(os.environ.get('DATABASE_URL'))

consumer_key = str(os.environ.get('consumer_key'))
consumer_secret = str(os.environ.get('consumer_secret'))
access_token = str(os.environ.get('access_token'))
access_token_secret = str(os.environ.get('access_token_secret'))


def get_breakdowns(provider='@SMRT_Singapore'):
    """ Get Breakdowns
    @SMRT_Singapore
    @SBSTransit_Ltd
    """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    final = {}

    # Get latest 20 tweets from SMRT_SINGAPORE
    result = api.user_timeline(provider, count=5)

    for tweet in result:

        # Only record the breakdowns/update
        if provider == '@SMRT_Singapore':
            detect = '[EWL]' in tweet.text or '[NSL]' in tweet.text
        else:
            detect = 'SORRY' in tweet.text.upper() and ('NEL' in tweet.text.upper() or 'DTL' in tweet.text.upper())

        if detect:
            output = {}
            created_at = (tweet.created_at + timedelta(hours=8)).strftime('%Y %b %d, at %I %M %S %p')
            output[tweet.id_str] = {'tweet':tweet.text,
                                    'created_at':created_at}
            final.update(output)

    return final


def all_breakdowns():
    """ all breakdowns """
    final = {}
    final.update(get_breakdowns('@SMRT_Singapore'))
    final.update(get_breakdowns('@SBSTransit_Ltd'))
    return final


def subscribe(user_id):
    """ subscribe to the database """
    db = dataset.connect(database_url)
    table = db['subscriptions_train']

    if table.find_one(id_user=user_id) is None:
        table.insert(dict(id_user=user_id))
        text_ = """This thread has succesfully subscribed to recieve Train Breakdown Notifications! \nI will send inform you as soon they happen!\n\n"""
        return text_
    else:
        return "This thread is already subscribed to recieve Train Breakdown Notifications!"


def unsubscribe(user_id):
    """ unsubscribe to the database """
    db = dataset.connect(database_url)
    table = db['subscriptions_train']

    if table.find_one(id_user=user_id) is None:
        return "This thread is not subscribed to recieve Train Breakdown Notifications!\n/subscribe_train@shiokbot to subscribe!"
    else:
        table.delete(id_user=user_id)
        return "This thread has been unsubscribed to recieve Train Breakdown Notifications :("


def get_all_users():
    """ get all users """
    db = dataset.connect(database_url)
    output = []
    for user in db['subscriptions_train']:
        output.append(user['id_user'])
    return output


def clear_db():
    """ Delete all users and promos """
    db = dataset.connect(database_url)
    db['subscriptions_train'].drop()
    db['train'].drop()


def get_new_breakdowns():
    """ Return Breakdown Notifications and Refresh DB"""
    db = dataset.connect(database_url)
    new_breakdown = all_breakdowns()

    table = db['train']

    """ Get New Breakdowns"""
    new = []
    for key, value in new_breakdown.items():

        if table.find_one(tweet_id=key) is None:
            new.append(key)
        else:
            pass

    """ Add to DB """
    for key in new:
        table.insert(dict(tweet_id=key,
                          tweet=new_breakdown[key]['tweet'],
                          created_at=new_breakdown[key]['created_at']))

    return new


def get_new_breakdowns_message():
    """ Return New Breakdowns """

    _all_breakdowns = all_breakdowns()
    new = get_new_breakdowns()

    if len(new) == 0:
        return None
    else:
        text_ = "<b>Train Breakdowns!</b>\n\n"

        for key in new:
            text_ += "<b>" + _all_breakdowns[key]['created_at'] + \
                     "</b> | Text - " + _all_breakdowns[key]['tweet']
            text_ += "\n\n"

        return text_
