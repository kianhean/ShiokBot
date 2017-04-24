""" SINGAPORE GOV API FUNCTIONS """

import os
import json
import requests
from haversine import haversine


def connnect_gov_api(url_string):
    """ Conntect to Gov and return request object """
    data_gov_api = str(os.environ.get('DATAGOV'))
    headers = {'api-key': data_gov_api}
    request = requests.get(url_string, headers=headers)

    return request


def taxi_get(send_long, send_lat):
    """ Get Taxi Updates """
    connnect_gov_api_r = connnect_gov_api('https://api.data.gov.sg/v1/transport/taxi-availability')
    data = json.loads(connnect_gov_api_r.text)

    # Create inputs
    current = (send_long, send_lat)
    count_number = 0
    thres = 0.2

    # Count Number of Taxis <= thres
    collect_taxis = []
    for coord in data['features'][0]['geometry']['coordinates']:
        if haversine(current, coord) <= thres:
            count_number += 1
            collect_taxis.append(coord)
    
    if count_number > 0:

        # Convert location to string
        current_str = ''
        for x in current[::-1]:
            current_str += str(x) + ","
        current_str = current_str[:-1] + "|flag-YOU-lg"

        # Taxis!
        taxi_str = '||'
        for y in collect_taxis:
            taxi_str_t = ''
            for x in y[::-1]:
                taxi_str_t += str(x) + ","
            taxi_str += taxi_str_t[:-1] + "||"
        taxi_str = taxi_str[:-2]

        # Create Map
        key = str(os.environ.get('MAPQUEST'))

        url = "https://beta.mapquestapi.com/staticmap/v5/map?key="+ key + "&locations=" + current_str + \
            taxi_str + "&type=dark&scalebar=true|bottom&size=@2x&zoom=16&defaultMarker=circle-start-sm"

        return {'count_number': count_number, 'url':url}

    else:

        return {'count_number': count_number, 'url':None}


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
    hourly = data['items'][0]['readings']['psi_twenty_four_hourly']
    timestampp = data['items'][0]['timestamp'][:19].replace("T", " ")

    # Create Response
    final_string = "<b>The 24 hourly PSI Reading at " + timestampp + " is actually</b> \n\n"

    for key in sorted(hourly):
        final_string  =  final_string + (str(key) + " " + \
                                        str(hourly[key]) + "\n")
    return final_string + "\nHotspots at our neighbours there are like that!"


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
                    "°C and a low of " + str(low_) + "°C\n\n<b>Forecast Next 12 Hrs</b>\n\n"

    # Add 12 hr cast
    nowcast = data['items'][0]['periods'][0]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + \
                                        " - " + str(nowcast[key]) + "\n")
    final_string = final_string + "\n<b>Forecast Tomorrow</b>\n\n"

    # Add 24 hr cast
    nowcast = data['items'][0]['periods'][1]['regions']
    for key in sorted(nowcast):
        final_string  =  final_string + (str(key) + " - " + str(nowcast[key]) + "\n")

    return final_string + "\nShow you radarrrr somemore! Got colour means raining!"
