import dataset
from urllib.request import urlopen
from bs4 import BeautifulSoup


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

        output[code[i].get_text()] = [e, d]

    return output


def subscribe(user_id):
    """ subscribe to the database """
    db = dataset.connect('sqlite:///database.db')
    table = db['subscriptions']

    if table.find_one(id=user_id) is None:
        table.insert(dict(id=user_id))
        text_ = """This thread has succesfully subscribed to recieve New Uber Codes! \n Every hour I will send you the latest Uber Promo Codes so that you can apply them first!"""
        return 
    else:
        return "You are already subscribed to recieve New Uber Codes!"


def unsubscribe(user_id):
    """ unsubscribe to the database """
    db = dataset.connect('sqlite:///database.db')
    table = db['subscriptions']

    if table.find_one(id=user_id) is None:
        return "You are not subcscribed to recieve New Uber Codes!"
    else:
        table.delete(id=user_id)
        return "You have been unsubscribed to recieve New Uber Codes!"


def get_all_users():
    """ get all users """
    db = dataset.connect('sqlite:///database.db')
    output = []
    for user in db['subscriptions']:
        output.append(user['id'])
    return output


def store_new():
    """ Return New Codes and Refresh DB"""
    db = dataset.connect('sqlite:///database.db')
    new_codes = get_code()

    table = db['promo']

    """ Get New Codes"""
    new = []
    for key, value in new_codes.items():

        if table.find_one(promo=key) is None:
            new.append(key)
        else:
            pass

    """ Refresh DB """
    table.drop()
    table2 = db['promo']

    for key, value in new_codes.items():
        table2.insert(dict(promo=key, desc=value[1], exp=value[0]))

    """ Return New Promos """
    if len(new) == 0:
        # Nothing new
        return None
    else:
        text_ = "<b> New Promo Codes Released! Apply Now! </b> \n\n"

        for key in new:
            text_ += "<b>" + key + "</b> | Expires - " + new_codes[key][0] + " | " + new_codes[key][1]
            text_ += "\n"

        return text_
