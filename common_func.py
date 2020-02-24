import requests
from global_var import *

def get_request(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params)
    except Exception as e:
        print('Невозможно подключиться к серверу. Проверьте ссылку или доступ в интернет')
        print(f'Ошибка: {e.__class__}')
        raise SystemExit
    return r

def get_list_of_devices(items, brand):
    list_of_devices = []
    for item in items:
        for i in item:
            list_of_devices.append({
                'name': brand + ' ' + i.find('a').get_text(),
                'link': HOST + i.find('a').get('href')
            })
    return list_of_devices