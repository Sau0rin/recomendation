import sqlite3

import requests
from bs4 import BeautifulSoup as BS

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61'
}
url = 'https://piazzaitalia.md'


def get_html(url_link):
    try:
        request = requests.get(url=url_link, headers=headers)
        return request
    except:
        print('Сайт не отвечает!')
        exit()


def get_links(html):
    soup = BS(html.text, 'html.parser')
    links = []

    items = soup.find_all('ul', class_='oct-menu-ul oct-menu-parent-ul list-unstyled')

    # Находим все сслылки
    for item in items:
        lis = item.find_all('li')
        for li in lis:
            links.append(li.find('a').get('href'))

    # Из сформированного списка удаляем ненужные ссылки
    for key, item in enumerate(links):
        str_link = item.replace(url, '')
        if str_link.count('/') == 1:
            links.pop(key)          # Удаляет ссылки по индексу

    # Вывести на экран окончательный список ссылок
    '''for link in links:
        print(link)'''

    return links


def parse_cards(html):
    soup = BS(html.text, 'html.parser')
    items = soup.find_all('div', class_='product-layout')
    new_links = []

    if len(items) == 0:
        return -1
    else:
        for item in items:
            # new_links.append(item.find('div', class_='us-module-img').find('a').get('href'))
            card = item.find('div', class_='us-module-img').find('a').get('href')
            new_links.append(card)
        return new_links


def parse_inner_cards(prod_link, html):
    soup = BS(html.text, 'html.parser')

    item = soup.find('div', class_='us-product-top')
    cards = []
    try:
        try:
            image_link = item.find('div', class_='us-product-left').find('a', class_='oct-gallery').find('img').get('src')
        except:
            image_link = '-'
        try:
            artikul = item.find('div', class_='us-product-info').find('li', class_='us-product-info-item us-product-info-item-sku').find('span' , class_='us-product-info-code').get_text()
        except:
            artikul = '-'
        try:
            price = item.find('div', class_='us-product-right').find('div', class_='us-price-actual').get_text()
        except:
            try:
                price = item.find('div', class_='us-product-right').find('div', class_='us-price-new').get_text()
            except:
                price = '-'
        try:
            property_1 = item.find('div', class_='us-product-right').find('div', class_='us-product-attr-cont').get_text()

            property_1 = property_1.split('\n')

            property_ = []
            for key, el in enumerate(property_1):
                if len(el) != 0:
                    property_.append(el)
            string = ''
            for i in range(0, len(property_)):
                if i != 0 and i % 2 == 0:
                    string += '\n'
                elif i % 2 != 0:
                    string += ' '

                string += property_[i]

        except Exception as ex:
            string = '-'

        cards = [{
            'artikul': artikul,
            'prod_link': prod_link,
            'image_link': image_link,
            'price': price,
            'property': string
        }]

        return cards
    except:
        print('\t\tНепредвиденнная ошибка!')


class SaveSQL:
    def __init__(self):
        self.conn = sqlite3.connect('myDatabase11.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cards
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            artikul integer,
            prod_link text, 
            image_link text,
            price integer, 
            property text)
        """)

    def SQL(self, items):
        for item in items:
            card = (
                item['artikul'],
                item['prod_link'],
                item['image_link'],
                item['price'],
                item['property']
            )

            self.cursor.execute('INSERT INTO Cards VALUES(NULL,?, ?, ?, ?, ?)', card)
            self.conn.commit()


def main():
    html = get_html(url)
    links = []

    all_cards = []

    if html.status_code == 200:     # Проверяем ответил ли нам сайт
        links = get_links(html)
    else:
        print('Проверьте соединение с интернетом.')
        return -1

    for link in links:
        page = 1
        new_url = link + '?page=' + str(page)        # Формируется ссылка с нужной страницой

        while True:
            try:
                print('Парсится: ' + new_url)
                request = get_html(new_url)
            except Exception as ex:
                print('Нет ответа, либо достигнут конец!')
            if request.status_code != 200:
                print('Конец')
                break
            elif request.status_code == 200:
                print('PARSE -> GOOD')
                cards = parse_cards(html=request)
                if cards == -1:
                    break
                else:
                    for card in cards:
                        request = get_html(card)
                        if request.status_code == 200:
                            card_1 = parse_inner_cards(card, request)
                            save = SaveSQL()
                            save.SQL(card_1)
                        else:
                            print('Что-то пошло не так.\nТовар не найден в магазине.')

            page += 1
            new_url = link + '?page=' + str(page)


if __name__ == '__main__':
    main()
