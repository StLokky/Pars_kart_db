from common_func import *


def get_samsung_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', id="listoftovar").find_all('a')
    bd_links = []
    old_item = []
    for item in items:
        if old_item == item.get('href'):
            continue

        old_item = item.get('href')
        bd_links.append({
            'name': item.get_text(),
            'title': item.get('title'),
            'link': HOST + item.get('href')
        })
    return bd_links


def get_sams_cart_param(items):
    cart_param = []
    c = 0
    for item in items:
        c += 1
        if c % 2 == 1:
            par_name = item.get_text()
            if par_name not in SAMS_CART_PARAM:
                SAMS_CART_PARAM.append(par_name)
        else:
            par_val = item.get_text()
            cart_param.append({
                'par_name': par_name,
                'par_val': par_val
            })
    # print('cart_param - ', cart_param)
    # print('KYO_CART_PARAM - ', KYO_CART_PARAM)
    return cart_param


def get_samsung_page_content(html, bd_link, count):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h5.find_next_siblings('ul')
    cartridge = []
    print(
        f'{count}. Обрабатываем картридж {bd_link["name"]} по ссылке {bd_link["link"]}...',
        end=' ')
    list_of_devices = get_list_of_devices(items)
    print(f'Получено {len(list_of_devices)} аппарата(ов)')

    items = soup.h4.find_previous_sibling('br')
    try:                                                # на 5 страницах раздела нестандартная разметка
        # разобраться позже или обработать 5 пустых записей
        type_cart = items.previous.replace('\r\n', '')
    except Exception as e:                              # "тип картриджа" - ручками
        type_cart = ''
        print(
            f'Ошибка получения типа картриджа в странице {COUNT}, картридж - {bd_link["name"]}')
        print(f'Ошибка: {e.__class__}')

    items = soup.find_all(border='1')[0].find_all('td')
    cart_param = get_sams_cart_param(items)

    cartridge.append({
        'count': count,
        'brand': 'Samsung',
        'name': bd_link["name"],
        'type_cart': type_cart,
        'type_cart_rus': bd_link['title'],
        'link': bd_link["link"],
        'devices': list_of_devices,
        'cart_param': cart_param
    })
    return cartridge


def parse_samsung(url):
    html = get_request(url)
    if html.status_code != 200:
        print('Ошибка открытия страницы - ', url)
        print(html)
        raise SystemExit

    print('Парсинт URLS с главной страницы Samsung...')
    bd_links = get_samsung_links(html.text)
    print(f'Готово. Собрано {len(bd_links)} ссылок.')
    print()

    start = 0
    stop = -1
    count = start
    bd_samsung = []
    for bd_link in bd_links:
        count += 1
        html = get_request(bd_link['link'])
        if html.status_code != 200:
            print('Ошибка открытия страницы - ', bd_link['link'])
            print(html)
            continue
        bd_samsung.append(get_samsung_page_content(html.text, bd_link, count))

    print('***************  SAMS_CART_PARAM  **************')
    print(len(SAMS_CART_PARAM))
    print(SAMS_CART_PARAM)
    # print()
    # print(bd_samsung[:3], end='\n\n')

    return bd_samsung
