import dataset
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_code(pos=0):
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
        return "This thread has succesfully subscribed!"
    else:
        return "You are already subscribed!"

def unsubscribe(user_id):
    """ unsubscribe to the database """
    db = dataset.connect('sqlite:///database.db')
    table = db['subscriptions']

    if table.find_one(id=user_id) is None:
        return "You are not subcscribed!"
    else:
        table.delete(id=user_id)
        return "You have been unsubscribed!"
