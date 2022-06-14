from datetime import datetime, date, timedelta
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
import requests
import pytz
from requests.adapters import HTTPAdapter

EPG_XML = ''

EPG_URL = 'https://digea.gr/wp-admin/admin-ajax.php'

TIMEZONE = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')

CHANNELS = {
    '100': ('digea.alpha.gr', 'ALPHA'),
    '300': ('digea.ant1.gr', 'ANT1'),
    '800': ('digea.openbeyond.gr', 'OPEN BEYOND'),
    '400': ('digea.mtv.gr', 'M.tv'),
    '600': ('digea.skai.gr', 'SKAI'),
    '700': ('digea.star.gr', 'STAR'),
    '900': ('digea.mega.gr', 'MEGA'),
    '5700': ('digea.alfa.gr', 'ALFA'),
    '5710': ('digea.centertv.gr', 'CENTER TV'),
    '5720': ('digea.deltatv.gr', 'DELTA TV'),
    '5725': ('digea.diktyotv.gr', 'DIKTYO TV'),
    '5730': ('digea.smileam.gr', 'SMILE A.M.'),
    '5735': ('digea.enachannel.gr', 'ENA CHANNEL'),
    '5755': ('digea.lydiatv.gr', 'LYDIA TV'),
    '5750': ('digea.orestiadatv.gr', 'ORESTIADA TV'),
    '5760': ('digea.tvrodopi.gr', 'TV RODOPI'),
    '5765': ('digea.starbellados.gr', 'STAR B. ELLADOS'),
    '5770': ('digea.thrakinet.gr', 'THRAKINET'),
    '5775': ('digea.tileepiloges.gr', 'TILE EPILOGES'),
    '5780': ('digea.aepsilonanmakthrakis.gr', 'a.Epsilon An. Mak. Thrakis'),
    '5790': ('digea.xanthichannel.gr', 'XANTHI CHANNEL'),
    '5850': ('digea.4e.gr', '4Ε'),
    '5855': ('digea.atlastv.gr', 'ATLAS TV'),
    '5860': ('digea.bergina.gr', 'BERGINA'),
    '5880': ('digea.europeone.gr', 'EUROPE ONE'),
    '5885': ('digea.aechannelthessaloniki.gr', 'AE CHANNEL THESSALONIKI'),
    '5905': ('digea.kanali9.gr', 'KANALI 9'),
    '5910': ('digea.nickelodeonplus.gr', 'NICKELODEON PLUS'),
    '5865': ('digea.diontv.gr', 'DION TV'),
    '5920': ('digea.eurochannel.gr', 'EURO CHANNEL'),
    '5925': ('digea.tv100.gr', 'TV 100'),
    '5922': ('digea.gnomitv.gr', 'GNOMI TV'),
    '6000': ('digea.diktyo.gr', 'DIKTYO'),
    '6005': ('digea.flashtv.gr', 'FLASH TV'),
    '6010': ('digea.osiosnikanor.gr', 'ΟΣΙΟΣ ΝΙΚΑΝΩΡ'),
    '6050': ('digea.topchannel.gr', 'TOP CHANNEL'),
    '6060': ('digea.westchannel.gr', 'WEST CHANNEL'),
    '7000': ('digea.arttv.gr', 'ART TV'),
    '7005': ('digea.axelwostv.gr', 'AXELWOS TV'),
    '7010': ('digea.bhmatv.gr', 'BHMA TV'),
    '7015': ('digea.corfutv.gr', 'CORFU TV'),
    '7050': ('digea.epirustv1.gr', 'EPIRUS TV1'),
    '7055': ('digea.itv.gr', 'ITV'),
    '7065': ('digea.starttv.gr', 'START TV'),
    '5000': ('digea.achaiachannel.gr', 'ACHAIA CHANNEL'),
    '5002': ('digea.arkadikitv.gr', 'ARKADIKI TV'),
    '5004': ('digea.axiontv.gr', 'AXION TV'),
    '5006': ('digea.besttv.gr', 'BEST TV'),
    '5012': ('digea.hlektratv.gr', 'HLEKTRA TV'),
    '5014': ('digea.ionianchannel.gr', 'IONIAN CHANNEL'),
    '5030': ('digea.lepanto.gr', 'LEPANTO'),
    '5048': ('digea.lychnos.gr', 'LYCHNOS'),
    '5034': ('digea.mesogeiostv.gr', 'MESOGEIOS TV'),
    '5036': ('digea.anet.gr', 'a.NET'),
    '5038': ('digea.ort.gr', 'ORT'),
    '5007': ('digea.plp.gr', 'PLP'),
    '5040': ('digea.rtpkentpo.gr', 'RTP KENTPO'),
    '5042': ('digea.super.gr', 'SUPER'),
    '5044': ('digea.superb.gr', 'SUPER B'),
    '5950': ('digea.astratv.gr', 'ASTRA TV'),
    '5955': ('digea.thessaliatv.gr', 'THESSALIA TV'),
    '5960': ('digea.trt.gr', 'TRT'),
    '5965': ('digea.tv10.gr', 'TV 10'),
    '5970': ('digea.smileplus.gr', 'SMILE PLUS'),
    '5100': ('digea.etv.gr', 'ETV'),
    '5104': ('digea.enake.gr', 'ENA K.E.'),
    '5108': ('digea.starke.gr', 'STAR K.E.'),
    '3074': ('digea.art.gr', 'ART'),
    '3000': ('digea.extrachannel.gr', 'EXTRA CHANNEL'),
    '3004': ('digea.action24.gr', 'ACTION24'),
    '3008': ('digea.atticatv.gr', 'ATTICA TV'),
    '3012': ('digea.bluesky.gr', 'BLUE SKY'),
    '3016': ('digea.channel9.gr', 'CHANNEL 9'),
    '3030': ('digea.aechannel.gr', 'AE CHANNEL'),
    '3034': ('digea.hightv.gr', 'HIGH TV'),
    '3038': ('digea.kontra.gr', 'KONTRA'),
    '3042': ('digea.madtv.gr', 'MAD TV'),
    '3060': ('digea.risetv.gr', 'RISE TV'),
    '3064': ('digea.nickelodeon.gr', 'NICKELODEON'),
    '3072': ('digea.smile.gr', 'SMILE'),
    '3068': ('digea.alert.gr', 'ALERT'),
    '7100': ('digea.notostv.gr', 'NOTOS TV'),
    '7105': ('digea.creta.gr', 'CRETA'),
    '7110': ('digea.kphthtv.gr', 'KPHTH TV'),
    '7115': ('digea.kphthtv1.gr', 'KPHTH TV 1'),
    '7130': ('digea.neatvcrete.gr', 'NEA TV CRETE'),
    '7135': ('digea.sitiatv.gr', 'SITIA TV'),
    '7140': ('digea.aetv.gr', 'AE TV'),
    '7150': ('digea.aigaiotv.gr', 'AIGAIOTV'),
    '7155': ('digea.dimotikitileorasiko.gr', 'DIMOTIKI TILEORASI KO'),
    '7160': ('digea.iridatv.gr', 'IRIDA TV'),
    '7170': ('digea.tharri.gr', 'THARRI'),
    '7175': ('digea.samiakitv.gr', 'SAMIAKI TV'),
    '7185': ('digea.kosmos.gr', 'KOSMOS'),
    '7205': ('digea.syrostv1.gr', 'SYROS TV1'),
    '7210': ('digea.volcano.gr', 'VOLCANO'),
    '5800': ('digea.alitheiatv.gr', 'ALITHEIA TV'),
    '5810': ('digea.patridatv.gr', 'PATRIDA TV'),
    '5815': ('digea.tvm.gr', 'TVM'),
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://digea.gr',
    'Referer': 'https://digea.gr/epg/',
}

MATRIX = [d for d in (datetime.now(pytz.timezone("Europe/Athens")).date() + timedelta(n)
                           for n in range(10))]


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
    

def get_data(day):
    data = {
        'action': 'get_events',
        'date': day.strftime('%Y-%m-%d')
    }
    
    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=5))
    
    res = s.post(EPG_URL, headers=HEADERS, data=data, timeout=2, verify=False)
    return res.json()


def generate():
    chc = []

    for d in MATRIX:
        json = get_data(d)
        for entry in json:
            nci = CHANNELS.get(entry['channel_id'], None)
            if not nci:
                continue
            if nci not in chc:
                chc.append(nci)
                _channel(nci[0], nci[1])
            start = datetime.fromisoformat(entry['actual_time']).strftime('%Y%m%d%H%M%S')
            _programme(start, nci[0], entry['title_gre'], entry['long_synopsis_gre'])

    global EPG_XML
    return EPG_XML
