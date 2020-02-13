
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import lxml.html as lh
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from lxml import etree
import urllib


def get_today_menu():

    url = "https://www.swfr.de/essen-trinken/speiseplaene/mensa-flugplatz/"
    html = requests.get(url).content.decode("utf-8")

    today = date.today()
    today_datestring = today.strftime('%d.%m.')
    search_string = today_datestring + '</h3>'

    # convert into html list of lines
    html_list = html.split('\n')

    for idx, line in enumerate(html_list):
        if search_string in line:
            essen_1_string = html_list[idx + 1]
            essen_2_string = html_list[idx + 2]

            essen_1 = essen_1_string.split('<br>')
            essen_2 = essen_2_string.split('<br>')

            essen_1 = [s for s in essen_1 if not s.startswith('<')]
            essen_2 = [s for s in essen_2 if not s.startswith('<')]
            essen_2 = [s for s in essen_2 if not s.startswith('enthält Allergene')]


            return essen_1, essen_2

    return None



