from urllib.request import urlopen
from bs4 import BeautifulSoup


def bann(code):
    """ If banned return True else False """
    ban_list = ['First Ride', 'New Customers', 'From SMU', 'From NTU',
                'From NUS', 'From SUTD', 'From SIM', 'First GrabHitch', 'New GrabPay',
                'First 2 Rides', 'First 4 Rides']

    for word in ban_list:
        if code.find(word) > 0:
            return True
    return False


def get_code_general(url='https://www.couponese.com/store/uber.com/'):
    """ Connect to Paged Promo Codes"""
    # Connect to Source
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    loop = soup.findAll("article", {"class" : "ov-coupon"})
    output = {}

    for square in loop:

        country = square.findAll("div")[1].findAll("img")[0]['title']

        try:
            square.findAll("span", {"class" : "ov-expired"})[0]
            expired = True
        except:
            expired = False

        if country == 'Singapore' and expired is False:

            code = square.findAll("div")[2].findAll("strong")[0].text
            desc = square.findAll("div")[3].findAll("div", {"class" : "ov-desc"})[0].text
            expiry = square.findAll("div")[3].findAll("div", {"class" : "ov-expiry"})[0].text[1:]

            if bann(desc) is False:
                output[code] = [expiry, desc]
    return output


def promo_loop(promo_list):
    """ Compose Message For Promo Codes! """
    final = ''
    for key in promo_list.keys():
        final += key + ", "
    output = '<b>Checking ' + final[:-2] + ' for Promos!</b>\n\n'

    # Loop thru Websites to Check
    for key, value in promo_list.items():

        result = get_code_general(value)

        # If there are promo codes
        if len(result) > 0:
            output += '<b>' + key + '</b>\n\n'

            # Loop thru Promo Codes
            for key, value in result.items():
                output += key + ' | Expires - ' + value[0] + ' | ' + value[1]

    return output
