import codecs
from xml.sax.saxutils import escape
from datetime import datetime
import pytz


def append(text):
    with codecs.open("epg-tmp.xml", "a", "utf-8") as f:
        f.write(text + '\n')


def push(channel_name, data):
    append('<channel id="{}">'.format(channel_name))
    append('<display-name>{}</display-name>'.format(escape(channel_name)))
    append('</channel>')
    
    timezone = datetime.now(pytz.timezone('Europe/Athens')).strftime('%z')

    for channel in data:
        start = datetime.fromtimestamp(channel['start_time'], pytz.timezone('Europe/Athens')).strftime('%Y%m%d%H%M%S')

        stop = ''

        if 'end_time' in channel:
            stop = 'stop="{} {}"'.format(datetime.fromtimestamp(channel['end_time'], pytz.timezone('Europe/Athens')).strftime('%Y%m%d%H%M%S'), timezone)

        append('<programme start="{} {}" {} channel="{}">'.format(start, timezone, stop, channel_name))
        append('<title lang="el">{}</title>'.format(escape(channel['title'])))
        append('<desc>{}</desc>'.format(escape(channel['description'])))
        append('</programme>')

    print(f'{channel_name} done')
    print('----------------------------------------')
