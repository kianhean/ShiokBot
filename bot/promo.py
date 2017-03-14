""" PROMO FUNCTIONS """

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_code(pos=0, smart=False):
    # Connect to Source
    url = 'https://www.cheapcheaplah.com/pages/grab-uber-taxi-promos'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    service = soup.findAll("div", {"class" : "domaincoupons"})[pos]

    code = service.findAll("strong")
    desc = service.findAll("a")
    expiry = service.findAll("span", {"class" : "expiry"})
    text_ = ""

    ban_list = ['First Ride', 'Selected Riders', 'New Customers', 'From SMU', 'From NTU',
                'From NUS', 'From SUTD', 'From SIM']

    for i in range(len(code) - 1, 0, -1):

        ban = False

        if smart is True:
            for ban_word in ban_list:
                if ban_word.upper() in desc[i].get_text().upper():
                    ban = True
                    break

        if ban is False:
            text_ += "<b>" + code[i].get_text() + "</b> | Expires - " + \
                     expiry[i].get_text() + " | " + desc[i].get_text() + "\n"
    return text_
