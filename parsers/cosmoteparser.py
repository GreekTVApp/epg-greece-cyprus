from datetime import datetime, timedelta
import pytz
import requests
import xmlutil
import os

URL = 'https://www.cosmotetv.gr/portal/residential/program?p_p_id=dayprogram_WAR_OTETVportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&_dayprogram_WAR_OTETVportlet_date={DATE}&_dayprogram_WAR_OTETVportlet_feedType=EPG&_dayprogram_WAR_OTETVportlet_start=0&_dayprogram_WAR_OTETVportlet_end=15&_dayprogram_WAR_OTETVportlet_platform=DTH&_dayprogram_WAR_OTETVportlet_categoryId=-1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Referer': 'https://www.cosmotetv.gr/portal/residential/program',
    'Origin': 'https://www.cosmotetv.gr/'
}

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')


def parse(channel, cosmote_cache):
    server_name = channel.get('serverName')
    epg_name = channel.get('epgName')
    print(f'{epg_name} start')

    channel_epg = []

    for date_diff in range(-1, 8):
        date_now = datetime.now(pytz.timezone("Europe/Athens")) + timedelta(days=date_diff)
        date_str = date_now.strftime('%d-%m-%Y')

        if date_str not in cosmote_cache:
            print(f'Cosmote: {date_str} not found, caching..')

            response = requests.get(URL.replace('{DATE}',date_str), headers=HEADERS, timeout=60)

            cosmote_cache[date_str] = response.json()

        json = cosmote_cache[date_str]

        day = json['currentDay']
        channel = list(filter(lambda x: x['ID'] == server_name, json['channels']))[0]
        programs = channel['shows']

        for program in programs:
            start_time_string = day + ' ' + program['startTime'] + ' ' + TIMEZONE
            start_time = datetime.strptime(start_time_string, '%d-%m-%Y %H:%M %z').timestamp()

            end_time_string = day + ' ' + program['endTime'] + ' ' + TIMEZONE
            end_time = datetime.strptime(end_time_string, '%d-%m-%Y %H:%M %z').timestamp()

            # If end time is less than start time, it means that the program ends on the next day
            if end_time < start_time:
                end_time = end_time + 86400

            program_object = {
                'channel': epg_name,
                'title': program['title'],
                'start_time': start_time,
                'end_time': end_time,
                'description': program['title']
            }

            channel_epg.append(program_object)

    icon = channel.get('icon')
    xmlutil.push(epg_name, channel_epg, icon)


