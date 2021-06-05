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
import urllib.parse
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
        """
        get start page with all query ads
        :param page:
        :return:
        """
        params = {
            # 'radius': 0,
            # 'user': 1
            'q': 'мкрн+зеленый'
        }
        if page and page > 1:
            params['p'] = page

        # https://www.avito.ru/irkutsk?q=мкрн+зеленый
        url = r'https://www.avito.ru/irkutsk/'
        r = self.session.get(url, params=params)
        print(r.status_code)
        return r.text
        pass

    @staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')
        if len(params) == 2:
            day, time = params
            if day == 'Сегодня':
                date = datetime.date.today()
            elif day == 'Вчера':
                date = datetime.date.today() - datetime.timedelta(days=1)
            else:
                print('Несмогли разобрать день: ', item)
                return ''
            time = datetime.datetime.strptime(time, '%H:%M').time()
            return datetime.datetime.combine(date=date, time=time)
        elif len(params) == 3:
            day, month_hru, time = params
            day = int(day)
            list_month = ['января', 'февраля', 'марта', 'апреля',
                          'мая', 'июня', 'июля', 'августа',
                          'сентября', 'октября', 'ноября', 'декабря']
            month_map = {i: j for i, j in zip(list_month, range(1, 13))}

            month = month_map.get(month_hru)
            if not month:
                print('не смогли разобрать месяы: ', item)
                return
            today = datetime.datetime.today()
            time = datetime.datetime.strptime(time, '%H:%M')
            return datetime.datetime(day=day, month=month, year=today.year, hour=time.hour, minute=time.minute)
        else:
            print('not remember date format')
            return

        pass

    def parse_block(self, item):
        url_block = item.get('a', {'data-marker': "item-title"})  # !!!!!!!!!!!!
        print(url_block)
        href = url_block.get('href')
        if href:
            url = r'https://www.avito.ru/irkutsk/' + href
        else:
            url = None

        title_block = item.select_one('h3', {'itemprop': "name"})
        title = title_block.string.strip()

        price_block = item.select_one('span.price-text-1HrJ_.text-text-1PdBw.text-size-s-1PUdo')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block) == 2:
            price, currency = price_block
        else:
            price, currency = None, None
            print('что-то пошло не так при поиске цены', price_block)

        date = None
        date_block = item.select_one('div.date-text-2jSvU.text-text-1PdBw.text-size-s-1PUdo.text-color-noaccent-bzEdI')
        absolute_date = date_block.get('date-absolute-date')
        if absolute_date:
            date = self.parse_date(item=absolute_date)

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=date
        )
        pass

    def get_pagination_number(self):
        text = self.get_page()
        soup = bs(text, 'lxml')
        container = soup.select('a.pagination-page')
        last_button = container[-1]
        href = last_button.get('href')
        if not href:
            return 1

        r = urllib.parse.urlparse(href)
        r = urllib.parse.parse_qs(r.query)
        return int(r['p'][0])
        pass

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)  # page=2
        soup = bs(text, 'lxml')
        container = soup.select('div.iva-item-root-G3n7v.photo-slider-slider-3tEix.'
                                'iva-item-list-2_PpT.iva-item-redesign-1OBTh.items-item-1Hoqq.'
                                'items-listItem-11orH.js-catalog-item-enum')
        print(len(container))
        for item in container:
            block = self.parse_block(item=item)
        pass

    def parse_all(self):
        limit = self.get_pagination_number()
        for i in range(1, limit + 1):
            self.get_blocks(page=1)
        pass





def main():
    p = AvitoParser()
    # p.get_page()
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
