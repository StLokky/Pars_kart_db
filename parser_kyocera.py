from common_func import *

def get_kyocera_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(colspan="2")
    bd_links = []
    for item in items:
        bd_links.append({
            'name': item.find('a').get_text(),
            'title': item.find('a').get('title').replace('Kyocera ', ''),
            'link': HOST + item.find('a').get('href')
        })
    return bd_links

def get_kyo_cart_param(items):
    cart_param = []
    c = 0
    for item in items:
        c += 1
        if c%2 == 1:
            par_name = item.get_text()
            if par_name not in KYO_CART_PARAM:
                KYO_CART_PARAM.append(par_name)
        else:
            par_val = item.get_text()
            cart_param.append({
                'par_name': par_name,
                'par_val': par_val
            })
    # print('cart_param - ', cart_param)
    # print('KYO_CART_PARAM - ', KYO_CART_PARAM)
    return cart_param

def get_kyocera_page_content(html, bd_link):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h5.find_next_siblings('ul')
    cartridge = []
    global COUNT
    print(f'{COUNT}. Обрабатываем картридж {bd_link["name"]} по ссылке {bd_link["link"]}...', end=' ')
    list_of_devices = get_list_of_devices(items)
    print(f'Получено {len(list_of_devices)} аппарата(ов)')

    items = soup.h4.find_previous_sibling('br')
    try:                                                # на 5 страницах раздела нестандартная разметка
        type_cart = items.previous.replace('\r\n','')   # разобраться позже или обработать 5 пустых записей
    except Exception as e:                              # "тип картриджа" - ручками
        type_cart = ''
        print(f'Ошибка получения типа картриджа в странице {COUNT}, картридж - {bd_link["name"]}')
        print(f'Ошибка: {e.__class__}')

    items = soup.find_all(border = '1')[0].find_all('td')
    cart_param = get_kyo_cart_param(items)


    cartridge.append({
        'count': COUNT,
        'brand': 'Kyocera',
        'name': bd_link["name"],
        'type_cart': type_cart,
        'type_cart_rus': bd_link['title'],
        'link': bd_link["link"],
        'devices': list_of_devices,
        'cart_param': cart_param
    })
    return cartridge


def parse_kyocera():
    html = get_request(URL_KYO)
    if html.status_code != 200:
        print('Ошибка открытия страницы - ', URL_KYO)
        print(html)
        raise SystemExit

    print('Парсинт URLS с главной страницы Kyocera...')
    bd_links = get_kyocera_links(html.text)
    print(f'Готово. Собрано {len(bd_links)} ссылок.')

    global COUNT
    COUNT = START
    for bd_link in bd_links:
        COUNT += 1
        html = get_request(bd_link['link'])
        if html.status_code != 200:
            print('Ошибка открытия страницы - ', bd_link['link'])
            print(html)
            continue
        BD_KYOCERA.append(get_kyocera_page_content(html.text, bd_link))

    print('***************  KYO_CART_PARAM  **************')
    print(KYO_CART_PARAM)
    return


def write_kyocera_csv():
    global BD_KYOCERA
    with open('kyocera.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow(['Картридж', 'Тип картриджа', 'Ссылка картриджа', 'Устройства' ])
        for item in BD_KYOCERA:
            devices = str_of_devices(item[0]['devices'])
            for i in item:
                writer.writerow([
                i['count'],
                i['brand'],
                i['name'],
                i['type_cart'],
                i['type_cart_rus'],
                i['link'],
                devices
                ])




parse_kyocera()
write_kyocera_csv()

write_kyocera_pickle(BD_KYOCERA, 'pickle_kyo.bd')
write_kyocera_json(BD_KYOCERA, 'json_kyo_bd.txt')

