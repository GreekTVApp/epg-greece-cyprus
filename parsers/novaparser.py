import requests
from datetime import datetime, timedelta
import pytz
import xmlutil
import json
import os

URL = 'https://api-web.forthnet-be.cdn.united.cloud/v1/public/events/epg'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Referer': 'https://epg.nova.gr/',
    'Origin': 'https://epg.nova.gr',
}

epg_token_url = 'https://api-web.forthnet-be.cdn.united.cloud/oauth/token?grant_type=client_credentials'

epg_token_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Authorization': os.environ['NOVA_TOKEN'],
    'Origin': 'https://epg.nova.gr',
    'Referer': 'https://epg.nova.gr/',
}

def parse(channel, nova_cache):
    server_name = channel.get('serverName')
    epg_name = channel.get('epgName')
    date_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')
    date_plus_seven = (datetime.utcnow() + timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')
    print(f'{epg_name} start')

    channel_epg = []

    if nova_cache == {}:
        print(f'NOVA: epg_token not found, caching..')
        response = requests.post(url=epg_token_url, headers=epg_token_headers)
        nova_cache['epg_token'] = response.json()['access_token']

    access_token = nova_cache['epg_token']
    HEADERS['Authorization'] = f'Bearer {access_token}'

    # https://api-web.forthnet-be.cdn.united.cloud/v1/public/events/epg?fromTime=2024-01-25T00:00:00%2B02:00&toTime=2024-02-04T23:59:59%2B02:00&communityId=35&languageId=164&cid=2
    params = {
        'fromTime': f'{date_today}+02:00',
        'toTime': f'{date_plus_seven}+02:00',
        'communityId': '35',
        'languageId': '164',
        'cid': server_name,
        'lang': 'el'
    }

    response = requests.get(url=URL, params=params, headers=HEADERS)
    res_json = response.json()

    for program in res_json.get(server_name, []):
        start_time_str = program.get('startTime')
        start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()

        end_time_str = program.get('endTime')
        end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()

        program_object = {
            'channel': epg_name,
            'title': program.get('title', 'N/A'),
            'start_time': start_time,
            'end_time': end_time,
            'description': program.get('shortDescription', 'N/A')
        }

        channel_epg.append(program_object)

    icon = channel.get('icon')
    xmlutil.push(epg_name, channel_epg, icon)
