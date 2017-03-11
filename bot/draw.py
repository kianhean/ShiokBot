""" Lucky Draw Methods """
from urllib.request import urlopen
from bs4 import BeautifulSoup


def FourD():
    """4D Methods!"""

    # Connect to Source
    url = 'https://www.gidapp.com/lottery/singapore/4d'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    result = soup.findAll('time')
    latest_result_date = result[6].get_text()

    result = soup.find_all('span')

    # TOP PRIZES
    first = result[8].get_text()
    second = result[9].get_text()
    third = result[10].get_text()

    top_text = "1st - " + first + "\n2nd - " + second + "\n3rd - " + third + "\n\n"

    # SPECIAL PRIZE
    special_prize = "Special/Starter Prizes\n\n"
    for i in range(11, 21):
        special_prize +=  result[i].get_text() + "  "

    # CONSOLATION PRIZE
    consol_prize = "\n\nConsolation Prizes\n\n"
    for i in range(21, 31):
        consol_prize +=  result[i].get_text() + "  "

    # Create Reply
    chat_reply = "Latest Draw Results on " + latest_result_date + " \n\n"
    chat_reply += top_text
    chat_reply += special_prize
    chat_reply += consol_prize
    chat_reply += "\n\n No need check la sure never win!"

    return chat_reply
