""" SINGAPORE GOV API FUNCTIONS """

import os
import json
import requests


def connnect_gov_api(url_string):
    """ Conntect to Gov and return request object """
    data_gov_api = str(os.environ.get('DATAGOV'))
    headers = {'api-key': data_gov_api}
    request = requests.get(url_string, headers=headers)

    return request


def traffic_get(location):
    """ Get Traffic Updates """

    connnect_gov_api_r = connnect_gov_api('https://api.data.gov.sg/v1/transport/traffic-images')
    data = json.loads(connnect_gov_api_r.text)

    if len(location) == 0:
        return 'Please enter either traffic Woodlands or traffic Tuas'
    else:
        location = str(location).upper()

    if location == 'TUAS':
        target_ = '4703' # Tuas
    elif location == 'WOODLANDS':
        target_ = '2701' # Woodlands
    else:
        return 'Sorry for now only understooded either Tuas or Woodlands!'

    # Get required data
    for data_ in data['items'][0]['cameras']:
        if (data_['camera_id']) == target_:
            img_url = data_['image']
            timestampp = data_['timestamp'][:19].replace("T", " ")

    # Create Response
    final_string = "The " + location.title() + " Checkpoint Situation at " + \
                   timestampp + " is like that la \n\n"

    final_string = final_string + '<a href="' +img_url+ '">Traffic Image!</a>'
    return final_string


def psi3hour_get():
    """ Get Latest Singapore PSI """

    connnect_gov_api_r = connnect_gov_api('https://api.data.gov.sg/v1/environment/psi')
    data = json.loads(connnect_gov_api_r.text)

    # Load data into Dictionary and get reading
    hourly = data['items'][0]['readings']['psi_three_hourly']
    timestampp = data['items'][0]['timestamp'][:19].replace("T", " ")

    # Create Response
    final_string = "The 3 hourly PSI Reading at " + timestampp + " is actually \n\n"
                    
    for key in sorted(hourly):
        final_string  =  final_string + (str(key) + " " + \
                                        str(hourly[key]) + "\n")
    return final_string + '<a href="http://wip.weather.gov.sg/wip/pp/gif/rghz.gif" > Haze Map </a>'


def weathernow_get():
    """ Get Latest Singapore Weather """
    connnect_gov_api_r = connnect_gov_api(
        'https://api.data.gov.sg/v1/environment/24-hour-weather-forecast')
    data = json.loads(connnect_gov_api_r.text)

    # Load data into Dictionary and get reading
    forecast = data['items'][0]['general']['forecast']
    high_ = data['items'][0]['general']['temperature']['high']
    low_ = data['items'][0]['general']['temperature']['low']

    # Create Response
    final_string = "In General the weather will be looking like " + forecast + \
                    " with a high of " + str(high_) + \
                    "°C and a low of " + str(low_) + "°C\n\nForecast Next 12 Hrs\n\n"

    # Add 12 hr cast
    nowcast = data['items'][0]['periods'][0]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + \
                                        " - " + str(nowcast[key]) + "\n")
    final_string = final_string + "\nForecast Tomorrow\n\n"

    # Add 24 hr cast
    nowcast = data['items'][0]['periods'][1]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + " - " + str(nowcast[key]) + "\n")

    return final_string + '<a href="http://www.ulfp.com/ulfp/txp_file/download.asp?SRC=download/ulfp/Animate/1_rad70d.gif" > Radar Map </a>'
