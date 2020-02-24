from common_func import *

from bs4 import BeautifulSoup
import csv

def get_kyocera_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(colspan="2")
    f_url = []
    for item in items:
        f_url.append({
            'name': item.find('a').get_text(),
            'title': item.find('a').get('title'),
            'link': HOST + item.find('a').get('href')
        })
    return f_url


def get_kyocera_page_content(html, name, link):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h5.find_next_siblings('ul')
    kart_for_devices = []
    global COUNT
    print(f'{COUNT}. Обрабатываем картридж {name} по ссылке {link}...', end=' ')
    list_of_devices = get_list_of_devices(items, 'Kyocera')

    kart_for_devices.append({
        'name': 'Kyocera ' + name,
        'link': link,
        'devices': list_of_devices
    })
    print(f'Получено {len(list_of_devices)} аппарата(ов)')
    COUNT += 1
    return kart_for_devices

def parse_kyocera():
    html = get_request(URL)
    if html.status_code != 200:
        print('Ошибка открытия страницы - ', URL)
        print(html)
        raise SystemExit

    print('Парсинт URLS с главной страницы Kyocera...')
    bd_links = get_kyocera_links(html.text)
    print(f'Готово. Собрано {len(bd_links)} ссылок.')

    for item in bd_links[START:STOP]:
        html = get_request(item['link'])
        if html.status_code != 200:
            print('Ошибка открытия страницы - ', item['link'])
            print(html)
            continue
        BD_KYOCERA.append(get_kyocera_page_content(html.text, item['name'], item['link']))


def str_of_devices(items):
    s = ''
    tstr = []
    for i in items:
        s = ''
        tstr = []
        for d in i['devices']:
            tstr.append(d['name'])
    s = ', '.join(tstr)
    return s


def write_kyocera_csv():
    global BD_KYOCERA
    with open('kyocera.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Картридж', 'Ссылка картриджа', 'Устройства'])
        for item in BD_KYOCERA:
            devices = str_of_devices(item)
            for i in item:
                writer.writerow([i['name'], i['link'], devices])


parse_kyocera()
write_kyocera_csv()


