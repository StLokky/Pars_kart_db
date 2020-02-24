import requests
from bs4 import BeautifulSoup

URL = 'http://rashodnika.net/10_1_1.html'  # Kyocera
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
HOST = 'http://rashodnika.net/'
BD_KYOCERA = []
count = 1

def get_html(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params)
    except Exception as e:
        print('Невозможно подключиться к серверу. Проверьте ссылку или доступ в интернет')
        print(f'Ошибка: {e.__class__}')
        raise SystemExit
    return r


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


def get_kyocera_page_content(html, name, brand, link):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h5
    items = items.find_next_siblings('ul')
    kart_for_prn = []
    list_of_prn = []
    global count
    print(f'{count}. Обрабатываем {name} по ссылке {link}...', end=' ')
    for item in items:
        for i in item:
            list_of_prn.append({
                'name': brand + ' ' + i.find('a').get_text(),
                'link': HOST + i.find('a').get('href')
            })
    kart_for_prn.append({
        'name': name,
        'link': link,
        'prns': list_of_prn
    })
    print(f'Получено {len(list_of_prn)} ')
    count += 1
    return kart_for_prn

def parse_kyocera():
    html = get_html(URL)
    if html.status_code != 200:
        print('Ошибка открытия страницы - ', URL)
        print(html)
        raise SystemExit

    print('Парсинт URLS с главной страницы Kyocera...')
    bd_links = get_kyocera_links(html.text)
    print(f'Готово. Собрано {len(bd_links)} ссылок.')

    for item in bd_links:
        html = get_html(item['link'])
        if html.status_code != 200:
            print('Ошибка открытия страницы - ', item['link'])
            print(html)
            continue
        BD_KYOCERA.append(get_kyocera_page_content(html.text, item['name'], 'Kyocera', item['link']))



parse_kyocera()

print(BD_KYOCERA[0])
print(BD_KYOCERA[4])
print(BD_KYOCERA[-1])
print(BD_KYOCERA[-2])
