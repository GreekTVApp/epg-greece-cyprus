from datetime import datetime, timedelta
import pytz
import requests
import xmlutil
import os

URL = 'https://digea.gr/wp-admin/admin-ajax.php'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Referer': 'https://digea.gr/epg/',
    'Origin': 'https://digea.gr'
}

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')


def parse(server_name, epg_name, digea_cache):
    print(f'{epg_name} start')

    channel_epg = []

    for date_diff in range(-1, 8):
        date_now = datetime.now(pytz.timezone("Europe/Athens")) + timedelta(days=date_diff)
        date_str = date_now.strftime('%Y-%m-%d')

        if date_str not in digea_cache:
            print(f'Digea: {date_str} not found, caching..')

            post_data = {
                'action': 'get_events',
                'date': date_str
            }

            response = requests.post(URL, headers=HEADERS, data=post_data, timeout=60, verify=os.path.abspath("parsers/digea.pem"))

            digea_cache[date_str] = response.json()

        json = digea_cache[date_str]

        programs = list(filter(lambda x: x['channel_id'] == server_name, json))

        for program in programs:
            start_time_string = program['actual_time'] + ' ' + TIMEZONE
            start_time = datetime.strptime(start_time_string, '%Y-%m-%d %H:%M:%S %z').timestamp()

            end_time_string = program['end_time'] + ' ' + TIMEZONE
            end_time = datetime.strptime(end_time_string, '%Y-%m-%d %H:%M:%S %z').timestamp()

            program_object = {
                'channel': epg_name,
                'title': program['title_gre'],
                'start_time': start_time,
                'end_time': end_time,
                'description': program['long_synopsis_gre']
            }

            channel_epg.append(program_object)

    xmlutil.push(epg_name, channel_epg)


