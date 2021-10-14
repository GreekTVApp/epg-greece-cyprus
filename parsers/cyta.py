from datetime import datetime, date, timedelta
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
import requests
import pytz

EPG_XML = ''

EPG_URL = 'https://data.cytavision.com.cy/epg/index.php?lang=el'

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')

CHANNELS = {
    'ch27': ('cyta.rik1.cy', 'RIK 1'),
    'ch28': ('cyta.rik2.cy', 'RIK 2'),
    'ch29': ('cyta.omega.cy', 'OMEGA'),
    'ch26': ('cyta.ant1.cy', 'ANT1 CY'),
    'ch30': ('cyta.sigma.cy', 'SIGMA'),
    'ch151': ('cyta.alpha.cy', 'ALPHA CY'),
    'ch39': ('cyta.plustv.cy', 'PLUS TV'),
    'ch54': ('cyta.capitaltv.cy', 'CAPITAL TV'),
    'ch32': ('cyta.extra.cy', 'EXTRA CY'),
    'ch152': ('cyta.tvmall.cy', 'TVMALL'),
    'ch166': ('cyta.smiletv.cy', 'SMILE TV CY'),
    'ch12': ('cyta.discovery.cy', 'DISCOVERY'),
    'ch15': ('cyta.discoveryscience.cy', 'DISCOVERY SCIENCE'),
    'ch102': ('cyta.animalplanet.cy', 'ANIMAL PLANET'),
    'ch184': ('cyta.bbcearth.cy', 'BBC EARTH'),
    'ch119': ('cyta.history.cy', 'HISTORY'),
    'ch101': ('cyta.id.cy', 'INVESTIGATION DISCOVERY'),
    'ch150': ('cyta.travel.cy', 'TRAVEL'),
    'ch100': ('cyta.tlc.cy', 'TLC'),
    'ch172': ('cyta.euronews.cy', 'EURONEWS'),
    'ch2': ('cyta.eurosport1.cy', 'EUROSPORT 1'),
    'ch23': ('cyta.eurosport2.cy', 'EUROSPORT 2'),
    'ch133': ('cyta.greekcinema.cy', 'GREEK CINEMA'),
    'ch44': ('cyta.cytavisionsports1.cy', 'Cytavision Sports 1'),
    'ch38': ('cyta.cytavisionsports2.cy', 'Cytavision Sports 2'),
    'ch36': ('cyta.cytavisionsports3.cy', 'Cytavision Sports 3'),
    'ch67': ('cyta.cytavisionsports5.cy', 'Cytavision Sports 5'),
    'ch34': ('cyta.cytavisionsports6.cy', 'Cytavision Sports 6'),
    'ch324': ('cyta.cytavisionsports7.cy', 'Cytavision Sports 7'),
    'ch327': ('cyta.cablenetsports1.cy', 'Cablenet Sports 1'),
    'ch328': ('cyta.cablenetsports2.cy', 'Cablenet Sports 2'),
    'ch333': ('cyta.primetelsports1.cy', 'Primetel Sports 1'),
    'ch334': ('cyta.primetelsports2.cy', 'Primetel Sports 2'),
    'ch335': ('cyta.primetelsports3.cy', 'Primetel Sports 3'),
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': '',
    'Connection': 'keep-alive',
    'Referer': 'https://www.cyta.com.cy/tv-guide',
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
    ahr = soup.find_all('a', attrs={'class': 'channel_link'})
    div = soup.find_all('div', attrs={'class': 'epgrow clearfix'})
    for idx, val in enumerate(ahr):
        cid = val['data-reveal-id']
        nci = CHANNELS.get(cid, None)
        if not nci:
            continue
        for program in div[idx].find_all("div", attrs={'class': 'program'}):
            _data = program.find_all("div", attrs={'class': 'data'})[0]
            _time = int(program['data-start'])
            _title = _data.h4.text.split(" ", 1)[1]
            _desc = _data.h4.next_sibling.strip()
            _start = '%s%s00' % (day.strftime('%Y%m%d'), str(int(_time/60)).zfill(2) + str(_time % 60).zfill(2))
            _programme(_start, nci[0], _title, _desc)


def get_data(day):
    params = {
        'site': 'cyprus',
        'day': day,
        'lang': 'el',
        'package': 'all',
        'category': 'all',
    }
    res = requests.get(EPG_URL, headers=HEADERS, params=params)
    res.encoding = 'utf-8'
    return res.text


def generate():
    for channel in CHANNELS:
        _channel(CHANNELS[channel][0], CHANNELS[channel][1])

    for d, n in ((datetime.now(pytz.timezone("Europe/Athens")).date() + timedelta(n), n) for n in range(8)):
        h = get_data(n)
        parse_html(h, d)

    global EPG_XML
    return EPG_XML
