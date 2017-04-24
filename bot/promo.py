""" PROMO FUNCTIONS """

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_code(pos=0, smart=False):
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
    text_ = ""

    ban_list = ['First Ride', 'Selected Riders', 'New Customers', 'From SMU', 'From NTU',
                'From NUS', 'From SUTD', 'From SIM', 'First GrabHitch', 'New GrabPay',
                'First 2 Rides']
    ban_list = ['First Ride', 'New Customers', 'From SMU', 'From NTU',
                'From NUS', 'From SUTD', 'From SIM', 'First GrabHitch', 'New GrabPay',
                'First 2 Rides']

    for i in range(len(code) - 1, 0, -1):

        ban = False

        if smart is True:
            for ban_word in ban_list:
                if ban_word.upper() in desc[i].get_text().upper():
                    ban = True
                    break

        if ban is False:
            try:
                e = expiry[i].get_text()
            except:
                e = ""
            try:
                d = desc[i].get_text()
            except:
                d = ""

            text_ += "<b>" + code[i].get_text() + "</b> | Expires - " + \
                    e + " | " + d
            # Generate Deep Link
            if pos == 1:
                deep_link = ' <a href="uber://?action=applyPromo&client_id=0WaekG8fxi5hhC-dF91xAF395YO8iRd3&promo=' + \
                             code[i].get_text() + '">' + " Apply Code!" + "</a>"
                text_ += deep_link + "\n"
            else:
                text_ += "\n"

    return text_


def get_code_normal(url, pos=0):
    """ Connect to non page coupons! """
    # Connect to Source
    #url = 'https://www.cheapcheaplah.com/pages/grab-uber-taxi-promos'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    service = soup.findAll("div", {"class" : "domaincoupons"})[pos]

    code = service.findAll("strong")
    desc = service.findAll("a")
    expiry = service.findAll("span", {"class" : "expiry"})
    text_ = ""

    for i in range(0, len(code) - 1):

        try:
            e = expiry[i].get_text()
        except:
            e = ""
        try:
            d = desc[i].get_text()
        except:
            d = ""

        text_ += "<b>" + code[i].get_text() + "</b> | Expires - " + \
                e + " | " + d + "\n"
    return text_
