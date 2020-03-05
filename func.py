import requests
from bs4 import BeautifulSoup
import pickle
import json
from tqdm import tqdm
# from time import sleep

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
}

HOST = 'http://rashodnika.net/'

ListBrands = ('Sharp', 'Xerox')

ListBrandsFull = ('Brother', 'Canon', 'Epson', 'HP', 'Konica_Minolta', 'Kyocera',
              'Lexmark', 'OKI', 'Panasonic', 'Ricoh', 'Samsung', 'Sharp', 'Xerox')

BrandsDB = {
    'Brother'   : {'laser': 'http://rashodnika.net/1_1_1.html', 'inkjet': 'http://rashodnika.net/1_1_3.html',
                    'matrix': None},
    'Canon'     : {'laser': 'http://rashodnika.net/2_1_1.html', 'inkjet': 'http://rashodnika.net/2_1_3.html',
                'matrix': None},
    'Epson'     : {'laser': 'http://rashodnika.net/3_1_1.html', 'inkjet': 'http://rashodnika.net/3_1_3.html',
                'matrix': 'http://rashodnika.net/3_1_2.html'},
    'HP'        : {'laser': 'http://rashodnika.net/4_1_1.html', 'inkjet': 'http://rashodnika.net/4_1_3.html',
                'matrix': None},
    'Konica_Minolta': {'laser': 'http://rashodnika.net/13_1_5.html', 'inkjet': None,
                'matrix': None},
    'Kyocera'   : {'laser': 'http://rashodnika.net/10_1_1.html', 'inkjet': None,
                'matrix': None},
    'Lexmark'   : {'laser': 'http://rashodnika.net/5_1_1.html', 'inkjet': 'http://rashodnika.net/5_1_3.html',
                'matrix': 'http://rashodnika.net/5_1_2.html'},
    'OKI'       : {'laser': 'http://rashodnika.net/6_1_1.html', 'inkjet': 'http://rashodnika.net/6_1_3.html',
            'matrix': 'http://rashodnika.net/6_1_2.html'},
    'Panasonic' : {'laser': 'http://rashodnika.net/7_1_1.html', 'inkjet': 'http://rashodnika.net/7_1_3.html',
                  'matrix': 'http://rashodnika.net/7_1_2.html'},
    'Ricoh'     : {'laser': 'http://rashodnika.net/12_1_5.html', 'inkjet': 'http://rashodnika.net/12_1_9.html',
              'matrix': None},
    'Samsung'   : {'laser': 'http://rashodnika.net/8_1_1.html', 'inkjet': 'http://rashodnika.net/8_1_3.html',
                'matrix': None},
    'Sharp'     : {'laser': 'http://rashodnika.net/11_1_1.html', 'inkjet': 'http://rashodnika.net/11_1_3.html',
              'matrix': None},
    'Xerox'     : {'laser': 'http://rashodnika.net/9_1_7.html', 'inkjet': 'http://rashodnika.net/9_1_3.html',
              'matrix': None},
}

GlobalCartParam = []

def write_data_to_file_pickle(data, filename):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
    except Exception as e:
        return e
    return 0


def write_data_to_file_json(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        return e
    return 0


def cBrand(name=None):  # возвращает одну запись BrandsDB бренда, или "None" если такой записи нет
    return {name: BrandsDB[name]} if name in BrandsDB else None


def get_html(url, headers=None, params=None):
    try:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            print('\nОшибка открытия страницы - ', url)
            print(f'Ошибка: {r}')
            raise SystemExit
    except Exception as e:
        print('\nНевозможно подключиться к серверу. Проверьте ссылку или доступ в интернет')
        print(f'URL - {url}')
        print(f'Ошибка: {e.__class__}')
        raise SystemExit
    return r.text


def db_get_brand(db):  # Возвращает название бренда (ключ словаря)
    return list(db.keys())[0]


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', id="listoftovar").find_all('a')
    bd_links = []
    old_item = ""
    for item in items:
        if old_item == item.get('href'): # Пропускаем уже полученный адрес, если дублируется...
            continue
        old_item = item.get('href')
        bd_links.append({
            'name': item.get_text(),
            'title': item.get('title'),
            'link': HOST + item.get('href')
        })
    return bd_links


def get_list_of_devices(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h5.find_next_siblings('ul')
    list_of_devices = []
    for item in items:
        for i in item:
            list_of_devices.append({
                'name': i.find('a').get_text(),
                'link': HOST + i.find('a').get('href')
            })
    return list_of_devices


def get_type_cart(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h4.find_previous_sibling('br')
    try:  # на некоторых страницах раздела нестандартная разметка
        type_cart = items.previous.replace('\r\n', '')  # разобраться позже или обработать  пустые записи вручную
    except Exception as e:
        type_cart = ''  # "тип картриджа" - ручками
        # print(f'\nОшибка: {e.__class__}')
    return type_cart if len(type_cart) > 3 else ''


def get_cart_param(html):
    global GlobalCartParam
    soup = BeautifulSoup(html, 'html.parser')
    cart_param = []
    try:
        items = soup.find_all(border='1')[0].find_all('td')
        c = 0
        for item in items:
            c += 1
            if c % 2 == 1:
                par_name = item.get_text()
                if par_name not in GlobalCartParam:
                    GlobalCartParam.append(par_name)
            else:
                par_val = ''
                for i in item.contents:
                    par_val = par_val + str(i)
                cart_param.append({'par_name': par_name,'par_val': par_val})
    except Exception as e:
        print(f'Ошибка в парсинге параметров - {e}')
        # cart_param.append({'par_name': 'Параметры','par_val': 'не определены'})
    return cart_param


def parse(db, ctype):
    brand = db_get_brand(db)  # Обрабатываем страницу бренда по типу картриджей
    url = db[brand][ctype]  #
    print(f'\n*******\nОбрабатываем - {brand} {ctype} {url}...')  #
    html = get_html(url, HEADERS)  # Собираем список картриджей
    bd_links = get_links(html)  # и линки на страницы каждого картриджа
    # bd_links = {'name': название картриджа,'title': тип по русски,'link': ссылка на страницу картриджа}
    print(f'\rСобрано {len(bd_links)} ссылок на картриджи                  ')  #

    # sleep(1)

    start = 0  # Это переменные для отладки
    stop = 5  # чтобы не парсить все картриджи
    count = start  # а только определенный срез
    cartridge = []
    with tqdm(total=len(bd_links)) as pbar:
        for bd_link in bd_links:
            count += 1
            # print(f'\n{count}. Обрабатываем картридж {bd_link["name"]} по ссылке {bd_link["link"]}...')

            html = get_html(bd_link['link'], HEADERS) # Открываем страницу с картриджем
            list_of_devices = get_list_of_devices(html)  # Собираем на странице список аппаратов у этого картриджа
            # {'name': 'название аппарата', 'link': 'ссылка на страницу аппарата'}
            # print(f'Получено {len(list_of_devices)} аппарата(ов)')

            type_cart = get_type_cart(html)      #  Получаем тип картриджа на английском, если есть...
            if not type_cart: type_cart = ''

            cart_param = get_cart_param(html) #  cart_param = {'par_name': par_name, 'par_val': par_val}

            cartridge.append({
                'count': count,
                'brand': brand,
                'name': bd_link["name"],
                'type_cart': type_cart,
                'type_cart_rus': bd_link['title'],
                'link': bd_link["link"],
                'devices': list_of_devices,
                'cart_param': cart_param
            })
            # print(f'Обработано {len(cartridge)} из {len(bd_links)} страниц')
            pbar.update(1)
    return cartridge

