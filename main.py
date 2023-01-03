from channels import channels
from parsers import digeaparser, cytaparser, ertflixparser, ant1euparser
import traceback
import xmlutil


def main():
    open('epg-tmp.xml', 'w').close()
    xmlutil.append('<?xml version="1.0" encoding="UTF-8" ?>')
    xmlutil.append('<tv generator-info-name="epg-greece-cyprus" '
                   'generator-info-url="https://github.com/GreekTVApp/epg-greece-cyprus">')

    digea_cache = {}

    for channel in channels:
        try:
            if channel.get("provider") == 'digea':
                digeaparser.parse(channel.get('serverName'), channel.get('epgName'), digea_cache)
            elif channel.get("provider") == 'cyta':
                cytaparser.parse(channel.get('serverName'), channel.get('epgName'))
            elif channel.get("provider") == 'ertflix':
                ertflixparser.parse(channel.get('serverName'), channel.get('epgName'))
            elif channel.get("provider") == 'ant1eu':
                ant1euparser.parse(channel.get('serverName'), channel.get('epgName'))
        except:
            traceback.print_exc()
            print(f'{channel.get("epgName")} error')
            print('----------------------------------------')

    xmlutil.append('</tv>')


if __name__ == '__main__':
    main()
