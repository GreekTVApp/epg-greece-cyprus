from parsers import digea, ert, cyta
import codecs


def main():
    digea_epg = digea.generate()
    ert_epg = ert.generate()
    cyta_epg = cyta.generate()

    final_xml = '<?xml version="1.0" encoding="UTF-8" ?>\n' \
                '<tv generator-info-name="EPG-GRCY" generator-info-url="https://github.com/1nikolas/EPG-GRCY">\n'

    final_xml += digea_epg + '\n'
    final_xml += ert_epg + '\n'
    final_xml += cyta_epg

    final_xml += '</tv>'

    with codecs.open("EPG-GRCY-tmp.xml", "w", "utf-8-sig") as f:
        f.write(final_xml)


if __name__ == '__main__':
    main()
