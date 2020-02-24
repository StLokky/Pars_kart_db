import requests
from bs4 import BeautifulSoup

URL = 'http://rashodnika.net/10_1_1.html'  # Kyocera
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
HOST = 'http://rashodnika.net/'


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

def get_kyocera_content(html):
    pass

def parse_kyocera():
    html = get_html(URL)
    print(html)
    if html.status_code == 200:
        f_url = get_kyocera_links(html.text)
    else:
        print('Ошибка открытия страницы - ', URL)
        raise SystemExit

    print(f'Обработана корневая страница: {len(f_url)} записей.')
    print('Первый    - ', f_url[0])
    print('Последний - ', f_url[-1])
    print()

    for item in f_url[:2]:
        print(item)

        html = get_html(item['link'])
        print(html)
        print()
        if html.status_code == 200:
            get_kyocera_content(html.text)
        else:
            print('Ошибка открытия страницы - ', item['link'])
            raise SystemExit




parse_kyocera()
