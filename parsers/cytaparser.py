import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import xmlutil

URL = 'http://data.cytavision.com.cy/xmldataout/channel_program_xml.php'

HEADERS = {
    'User-Agent': 'Android Application',
    'Accept-Encoding': 'gzip'
}

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')


def parse(server_name, epg_name):
    print(f'{epg_name} start')

    channel_epg = []

    for day in range(-1, 8):
        params = {
            'days': day,
            'service_id': server_name,
            'lang': 'el'
        }

        response = requests.get(url=URL, params=params, headers=HEADERS)
        response.encoding = response.apparent_encoding
        xml_text = response.text
        xml = BeautifulSoup(xml_text, 'xml')
        programs = xml.find_all('r')

        for program in programs:
            title = program.find('Title').text
            start_time_str = program.find('StartTime').text + ' ' + TIMEZONE
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S %z').timestamp()
            end_time_str = program.find('EndTime').text + ' ' + TIMEZONE
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S %z').timestamp()
            description = program.find('Description').text

            program_object = {
                'channel': epg_name,
                'title': title,
                'start_time': start_time,
                'end_time': end_time,
                'description': description
            }

            channel_epg.append(program_object)

    xmlutil.push(epg_name, channel_epg)
