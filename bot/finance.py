
import json
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup


def get_sti():
    # https://github.com/hongtaocai/googlefinance
    return '<a href="https://chart.finance.yahoo.com/t?s=%5eSTI&lang=en-SG&region=SG&width=300&height=180" >'


def get_fx():
    url = 'https://eservices.mas.gov.sg/api/action/datastore/search.json?resource_id=95932927-c8bc-4e7a-b484-68a66a24edfe&limit=1&sort=end_of_day%20desc'
    request = requests.get(url)

    data = json.loads(request.text)
    result_today = data['result']['records'][0]

    AUD = 1/float(result_today['aud_sgd'])*1
    CNY = 1/float(result_today['cny_sgd_100'])*100
    HKD = 1/float(result_today['hkd_sgd_100'])*100
    EUR = 1/float(result_today['eur_sgd'])*1
    JPY = 1/float(result_today['jpy_sgd_100'])*100
    MYR = 1/float(result_today['myr_sgd_100'])*100
    THB = 1/float(result_today['thb_sgd_100'])*100
    TWD = 1/float(result_today['twd_sgd_100'])*100
    USD = 1/float(result_today['usd_sgd'])*1
    VND = 1/float(result_today['vnd_sgd_100'])*100

    list_curr = {'AUD': AUD, 'CNY':CNY, 'HKD':HKD, 'EUR':EUR, 'JPY':JPY,
                 'MYR':MYR, 'THB':THB, 'TWD':TWD, 'USD':USD, 'VND':VND}

    text_final = '<b>Latest SGD End of Day Rates ' + result_today['end_of_day'] + '</b>\n\n'

    for key in sorted(list_curr.keys()):
        text_final += key + " " + str(round(list_curr[key], 3)) + " = 1 SGD \n"
    return text_final


def get_sibor():
    # Connect to Source
    url = 'http://www.moneysmart.sg/home-loan/sibor-trend'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    result = soup.findAll("div", {"class" : "sibor-sor-table"})
    result = result[0].findAll("td")
    result = result[1:]

    text_final = '<b>Latest SIBOR Rates</b>\n\n'
    name = result[0:][::2]
    rate = result[1:][::2]

    for i in range(0, 4):
        text_final += name[i].get_text() + " - " + rate[i].get_text() + "\n"
    return text_final
