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
import datetime
# from collections import Counter
from collections import namedtuple

URL_AVITO_IRK: str = r'https://www.avito.ru/irkutsk/'
QUEST_INFO: str = r'nedvizhimost?' \
                  r'q=%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%80%D0%B0%D0%B9%D0%BE%D0%BD+' \
                  r'%D0%97%D0%B5%D0%BB%D1%91%D0%BD%D1%8B%D0%B9'

InnerBlock = namedtuple('Block', 'title,price,currency,date,url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'


class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'accept': '*/*',
            'accept-language': 'ru-RU'
        }

    def get_page(self, page: int = None):
        params = {
            'radius': 0,
            'user': 1
        }
        if page and page > 1:
            params['p'] = page

        url = r'https://www.avito.ru/irkutsk/'
        r = self.session.get(url, params=params)
        pass

    @staticmethod
    def parse_date(items: str):
        params = items.strip().split(' ')
        if len(params) == 2:
            day, time = params
            if day == 'Сегодня':
                date = datetime.date.today()
            elif day == 'Вчера':
                date = datetime.date.today() - datetime.timedelta(days=1)
            else:
                print('Несмогли разобрать день: ', items)
                return ''
            time = datetime.datetime.strptime(time, '%H:%M').time()
            return datetime.datetime.combine(date=date, time=time)

        pass

    def parse_block(self, item: str = None):
        pass

    def get_blocks(self):
        text = self.get_page(page=2)
        soup = bs(text, 'lxml')
        container = soup.select('div')
        for item in container:
            block = self.parse_block(item=item)
            print(block)
        pass

def main():
    p = AvitoParser()
    p.get_blocks()


if __name__ == '__main__':
    main()
    pass









# def get_request(utl):
#     response = requests.get(utl)
#
#     if response.status_code == '200':
#         return response
#     else:
#         raise Exception('Not 200 response')
#
#
# def get_count_page(response):
#     html_text = response.text
#     # class="pagination-root-2oCjZ"
#     # /html/body/div[1]/div[3]/div[3]/div[3]/div[5]/div[1]
#     # /html/body/div[1]/div[3]/div[3]/div[3]/div[5]/div[1]/span[8]
#
#     # find need page !!!!!!!!!!
#     pass
#
#
# def get_page_data(url_ads):
#     pass
#
#
# def writer_csv(data_avito):
#     pass
#
#
# def main():
#     pass
#
#
# if __name__ == '__main__':
#     pass
