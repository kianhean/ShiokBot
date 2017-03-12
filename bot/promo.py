""" PROMO FUNCTIONS """

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_code(pos=0):
    # Connect to Source
    url ='https://www.cheapcheaplah.com/pages/grab-uber-taxi-promos'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    service = soup.findAll("div", { "class" : "domaincoupons" })[pos]

    code = service.findAll("strong")
    desc = service.findAll("a")
    expiry = service.findAll("span", { "class" : "expiry" })
    text_ = ""
    
    for i in range(len(code) - 1, 0, -1):
        text_ += "<b>" + code[i].get_text() + "</b> | Expires - " + expiry[i].get_text() + " | " + desc[i].get_text() + "\n"
    return text_
