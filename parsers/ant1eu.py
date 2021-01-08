from datetime import datetime, date, timedelta
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
import requests
import pytz

EPG_XML = ''

EPG_URL = 'https://www.antennaeurope.gr/el/tvguide.html'

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')

CHANNEL = 'ant1eu.ant1europe.eu'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.antennaeurope.gr/el/tvguide.html',
}


def append(text):
    global EPG_XML
    EPG_XML += text + '\n'


def _programme(start, channel, title, desc):
    append('  <programme start="{} {}" channel="{}">'.format(start, TIMEZONE, channel))
    append('    <title lang="el">{}</title>'.format(escape(title)))
    append('    <desc>{}</desc>'.format(escape(desc)))
    append('  </programme>')


def _channel(channel, name):
    append('  <channel id="{}">'.format(channel))
    append('    <display-name lang="el">{}</display-name>'.format(escape(name)))
    append('  </channel>')


def parse_html(html, day):
    soup = BeautifulSoup(html, 'lxml')

    allEpg = soup.find_all('div', attrs={'class': 'shows col-12 col-sm-10 sentoni'})[0]

    tempDay = day

    isPastMidnight = False

    for singleEpg in allEpg.find_all('dl'):

        timeWithL = singleEpg.find_all('dt')[0]
        time = next(timeWithL.children).strip()

        timeobject = datetime.strptime(time, '%H:%M')

        if not isPastMidnight and 0 <= timeobject.hour < 6:
            isPastMidnight = True
            tempDay = tempDay + timedelta(1)

        dateandtime = tempDay.strftime("%Y%m%d") + time.replace(':', '') + '00'

        title = singleEpg.find_all('dd')[0].text.strip()

        _programme(dateandtime, CHANNEL, title, title)


def get_data(day):
    data = {
        'date': day.strftime('%Y-%m-%d'),
    }
    res = requests.post(EPG_URL, headers=HEADERS, params=data)
    res.encoding = 'UTF-8'
    return res.text


def generate():
    _channel(CHANNEL, 'ANT1 EUROPE')

    for d in (datetime.now(pytz.timezone("Europe/Athens")).date() + timedelta(n) for n in range(7)):
        h = get_data(d)
        parse_html(h, d)

    global EPG_XML
    return EPG_XML
