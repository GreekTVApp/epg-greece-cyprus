from parsers import digea, ert, cyta, ant1eu
import codecs


def main():
    digea_epg = digea.generate()
    ert_epg = ert.generate()
    cyta_epg = cyta.generate()
    ant1eu_epg = ant1eu.generate()

    final_xml = '<?xml version="1.0" encoding="UTF-8" ?>\n' \
                '<tv generator-info-name="epg-greece-cyprus" generator-info-url="https://github.com/GreekTVApp/epg-greece-cyprus">\n'

    final_xml += digea_epg + '\n'
    final_xml += ert_epg + '\n'
    final_xml += cyta_epg + '\n'
    final_xml += ant1eu_epg

    final_xml += '</tv>'

    with codecs.open("EPG-GRCY-tmp.xml", "w", "utf-8-sig") as f:
        f.write(final_xml)


if __name__ == '__main__':
    main()
