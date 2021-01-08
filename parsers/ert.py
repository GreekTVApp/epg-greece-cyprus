from datetime import datetime, date, timedelta
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
import requests
import pytz

EPG_XML = ''

EPG_URL = 'https://program.ert.gr/search.asp'

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')

CHANNELS = {
    '8': ('ert.vouli.gr', 'VOULI'),
    '9': ('ert.ert1.gr', 'ERT 1'),
    '10': ('ert.ert3.gr', 'ERT 3'),
    '11': ('ert.ertworld.gr', 'ERT WORLD'),
    '24': ('ert.ertsports.gr', 'ERT SPORTS'),
    '49': ('ert.ert2.gr', 'ERT 2'),
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.program.ert.gr',
    'Connection': 'keep-alive',
    'Referer': 'https://program.ert.gr/search.asp',
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
    chc = []
    _last_time = -1
    prevday = day
    nextday = day + timedelta(1)

    for ahr in soup.find_all('a', attrs={'class': 'black'}):
        cid = ahr['href'].rsplit('=', 1)[-1]
        nci = CHANNELS.get(cid, None)
        if not nci:
            continue
        if nci not in chc:
            chc.append(nci)
            _last_time = -1
            day = prevday
        atr = ahr.find_parent('tr', attrs={'bgcolor': True})
        _time = atr.td.text.strip().replace(':', '')
        _title = " ".join(atr.table.tr.text.split())
        _desc = atr.font and atr.font.text.strip() or _title
        if _last_time > int(_time):
            day = nextday
        _last_time = int(_time)
        _start = '%s%s00' % (day.strftime('%Y%m%d'), _time)
        _programme(_start, nci[0], _title, _desc)


def get_data(day):
    data = {
        'frmDates': day.strftime('%j'),
        'frmChannels': '',
        'frmSearch': '',
        'x': '14',
        'y': '6'
    }
    res = requests.post(EPG_URL, headers=HEADERS, data=data)
    res.encoding = 'windows-1253'
    return res.text


def generate():
    for channel in CHANNELS:
        _channel(CHANNELS[channel][0], CHANNELS[channel][1])

    for d in (datetime.now(pytz.timezone("Europe/Athens")).date() + timedelta(n) for n in range(11)):
        h = get_data(d)
        parse_html(h, d)

    global EPG_XML
    return EPG_XML
