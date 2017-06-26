import os
import dataset
from urllib.request import urlopen
from bs4 import BeautifulSoup

database_url = 'sqlite:///database.db'
database_url = str(os.environ.get('DATABASE_URL'))


def bann(code):
    """ If banned return True else False """
    ban_list = ['First Ride', 'New Customers', 'From SMU', 'From NTU',
                'From NUS', 'From SUTD', 'From SIM', 'First GrabHitch', 'New GrabPay',
                'First 2 Rides', 'First 4 Rides']

    for word in ban_list:
        if code.find(word) > 0:
            return True
    return False


def clear_db():
    """ Delete all users and promos """
    db = dataset.connect(database_url)
    db['subscriptions'].drop()
    db['promo'].drop()


def get_code(pos=1):
    """ Connect to Paged Promo Codes"""
    # Connect to Source
    url = 'https://www.cheapcheaplah.com/pages/grab-uber-taxi-promos'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    service = soup.findAll("div", {"class" : "domaincoupons"})[pos]
    code = service.findAll("strong")
    desc = service.findAll("a")
    expiry = service.findAll("span", {"class" : "expiry"})

    output = {}

    for i in range(len(code) - 1, 0, -1):

        try:
            e = expiry[i].get_text()
        except:
            e = ""
        try:
            d = desc[i].get_text()
        except:
            d = ""

        if bann(d) is False:
            output[code[i].get_text()] = [e, d]

    return output


def subscribe(user_id):
    """ subscribe to the database """
    db = dataset.connect(database_url)
    table = db['subscriptions']

    if table.find_one(id_user=user_id) is None:
        table.insert(dict(id_user=user_id))
        text_ = """This thread has succesfully subscribed to recieve New Uber Codes! \nI will send you the latest Uber Promo Codes when they get released so that you can apply them first!\n\n"""
        text_ += """These are the latest codes right now\n\n"""
        new_codes = get_code()

        for key in new_codes:
            text_ += "<b>" + key + "</b> | Expires - " + new_codes[key][0] + " | " + new_codes[key][1]
            text_ += "\n"
        return text_
    else:
        return "This thread is already subscribed to recieve New Uber Codes!"


def unsubscribe(user_id):
    """ unsubscribe to the database """
    db = dataset.connect(database_url)
    table = db['subscriptions']

    if table.find_one(id_user=user_id) is None:
        return "This thread is not subscribed to recieve New Uber Codes!\n/subscribe@shiokbot to subscribe!"
    else:
        table.delete(id_user=user_id)
        return "This thread has been unsubscribed to recieve New Uber Codes :("


def get_all_users():
    """ get all users """
    db = dataset.connect(database_url)
    output = []
    for user in db['subscriptions']:
        output.append(user['id_user'])
    return output


def get_new_codes():
    """ Return New Codes and Refresh DB"""
    db = dataset.connect(database_url)
    new_codes = get_code()

    table = db['promo']

    """ Get New Codes"""
    new = {}

    for key, value in new_codes.items():

        if table.find_one(promo=key) is None:
            new[key] = [new_codes[key][0], new_codes[key][1]]
        else:
            pass

    """ Add to DB """
    for key in new:
        table.insert(dict(promo=key, desc=new_codes[key][1], exp=new_codes[key][0]))

    return new


def get_new_codes_message():
    """ Return New Promos """
    new = get_new_codes()

    if len(new) == 0:
        return None
    else:
        text_ = "<b>New Promo Codes Released! Apply Now!</b>\n\n"

        for key, value in new.items():
            text_ += "<b>" + key + "</b> | Expires - " + value[0] + " | " + value[1]
            text_ += "\n"

        return text_
