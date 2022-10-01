import requests
from datetime import datetime, timedelta
import pytz
import xmlutil
import json

URL_PARAMS = '?$headers={"Content-Type":"application/json;charset=utf-8","X-Api-Date-Format":"unix",' \
             '"X-Api-Camel-Case":true}'

URL = 'https://api.app.ertflix.gr/v1/EpgTile/FilterProgramTiles' + URL_PARAMS

URL_TILES = 'https://api.app.ertflix.gr/v2/Tile/GetTiles' + URL_PARAMS

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Referer': 'https://www.ertflix.gr/',
    'Origin': 'https://www.ertflix.gr'
}


def parse(server_name, epg_name):
    print(f'{epg_name} start')

    channel_epg = []

    start_date = datetime.now(pytz.timezone('Europe/Athens')) + timedelta(days=-1)

    end_date = datetime.now(pytz.timezone('Europe/Athens')) + timedelta(days=8)

    post_data = {
        'platformCodename': 'www',
        'from': start_date.strftime('%Y-%m-%d') + "T02:00:00.000Z",
        'to': end_date.strftime('%Y-%m-%d') + "T02:00:00.000Z",
        'orChannelCodenames': [server_name]
    }

    response = requests.post(URL, headers=HEADERS, data=json.dumps(post_data))
    res_json = response.json()

    ids = [d['id'] for d in res_json['programs'][server_name]]

    post_data_tiles = {
        "platformCodename": "www",
        "requestedTiles": [{'id': i} for i in ids]
    }

    response2 = requests.post(URL_TILES, headers=HEADERS, data=json.dumps(post_data_tiles))

    tiles = response2.json()['tiles']

    for tile in tiles:

        subtitle = ''
        description = ''

        if 'subTitle' in tile:
            subtitle = tile['subTitle'] + '\n'

        if 'description' in tile:
            description = tile['description']

        program_object = {
            'channel': epg_name,
            'title': tile['title'],
            'start_time': tile['start'] / 1000,
            'end_time': tile['stop'] / 1000,
            'description': subtitle + description
        }

        channel_epg.append(program_object)

    xmlutil.push(epg_name, channel_epg)






