from datetime import datetime, timedelta
import requests
import pytz
from bs4 import BeautifulSoup
import xmlutil

URL = 'https://www.antennaeurope.gr/el/tvguide.html'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.antennaeurope.gr/el/tvguide.html',
}


def parse(server_name, epg_name):
    print(f'{epg_name} start')

    channel_epg = []

    for day in (datetime.now(pytz.timezone("Europe/Athens")) + timedelta(n) for n in range(7)):
        data = {
            'date': day.strftime('%Y-%m-%d'),
        }
        res = requests.post(URL, headers=HEADERS, params=data)
        res.encoding = 'UTF-8'

        html = res.text

        soup = BeautifulSoup(html, 'lxml')

        all_epg = soup.find_all('div', attrs={'class': 'shows col-12 col-sm-10 sentoni'})[0]

        temp_day = day

        is_past_midnight = False

        for singleEpg in all_epg.find_all('dl'):

            time_with_l = singleEpg.find_all('dt')[0]
            time = next(time_with_l.children).strip()

            time_object = datetime.strptime(time, '%H:%M')

            if not is_past_midnight and 0 <= time_object.hour < 6:
                is_past_midnight = True
                temp_day = temp_day + timedelta(1)

            start_time = temp_day.replace(hour=time_object.hour, minute=time_object.minute, second=0, microsecond=0)

            title = singleEpg.find_all('dd')[0].text.strip()

            program_object = {
                'channel': epg_name,
                'title': title,
                'start_time': start_time.timestamp(),
                'description': ''
            }

            channel_epg.append(program_object)

    xmlutil.push(epg_name, channel_epg)
