import csv
from collections import namedtuple
import requests
from lxml import etree

TWSE_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
# Marketable securities (MS)
MS = namedtuple("MS", [
    "MSType", "code", "name", "ISIN", "ListingDate", "market",
    "IndustrialClass", "CFIcode"
])


def stockListGen(path):
    """TWSE securities list generator.

    """
    response = requests.get(TWSE_EQUITIES_URL)
    root_node = etree.HTML(response.text)
    tr_nodes = root_node.xpath("//tr")[1:]

    ms_list = []
    ms_type = ''

    for tr_node in tr_nodes:
        td_list = list(map(lambda td_node: td_node.text, tr_node.iter()))
        if len(td_list) == 4:
            # The type of marketable securites (MS)
            ms_type = td_list[2].strip(' ')
        else:
            # MS information
            code, name = td_list[1].split('\u3000')
            ms_list.append(MS(ms_type, code, name, *td_list[2:-1]))

    with open(path, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # Write title row
        writer.writerow(ms_list[0]._fields)
        # Write data rows
        for ms in ms_list:
            writer.writerow([_ms for _ms in ms])


if __name__ == "__main__":
    stockListGen("stock-list.csv")
