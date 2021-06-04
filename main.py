#!/usr/bin/env python3
# -*- coding: utf8 -*-

# ---------------------------------------------
# Program by Vadim 2011
#
#
# Version    Date            Info
# 0.1        03.06.2021      Parser Avito
#
# план:
# 1. определить колличество страниц
# 2. сформировать список url
# 3. собрать данные
# 4. сохранить в csv file
# ---------------------------------------------
# 'https://www.avito.ru/irkutsk/nedvizhimost?q=%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%80%D0%B0%D0%B9%D0%BE%D0%BD+%D0%97%D0%B5%D0%BB%D1%91%D0%BD%D1%8B%D0%B9'

import requests
from bs4 import BeautifulSoup as bs

URL_AVITO_IRK: str = r'https://www.avito.ru/irkutsk/'
QUEST_INFO: str = r'nedvizhimost?' \
                  r'q=%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%80%D0%B0%D0%B9%D0%BE%D0%BD+' \
                  r'%D0%97%D0%B5%D0%BB%D1%91%D0%BD%D1%8B%D0%B9'


def get_request(utl):
    response = requests.get(utl)

    if response.status_code == '200':
        return response
    else:
        raise Exception('Not 200 response')


def get_count_page(response):
    html_text = response.text
    # class="pagination-root-2oCjZ"
    # /html/body/div[1]/div[3]/div[3]/div[3]/div[5]/div[1]
    # /html/body/div[1]/div[3]/div[3]/div[3]/div[5]/div[1]/span[8]

    # find need page !!!!!!!!!!
    pass


def get_page_data(url_ads):
    pass


def main():
    pass


if __name__ == '__main__':
    pass

