from common_func import *

def get_kyocera_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(colspan="2")
    f_url = []
    for item in items:
        f_url.append({
            'name': item.find('a').get_text(),
            'title': item.find('a').get('title').replace('Kyocera ', ''),
            'link': HOST + item.find('a').get('href')
        })
    return f_url


def get_kyocera_page_content(html, bd_link):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.h5.find_next_siblings('ul')
    cartridge = []
    global COUNT
    print(f'{COUNT}. Обрабатываем картридж {bd_link["name"]} по ссылке {bd_link["link"]}...')
    list_of_devices = get_list_of_devices(items)

    items = soup.h4.find_previous_sibling('br')
    type_cart = items.previous.replace('\r\n','')


    cartridge.append({
        'brand': 'Kyocera',
        'name': bd_link["name"],
        'type_cart': type_cart,
        'type_cart_rus': bd_link['title'],
        'link': bd_link["link"],
        'devices': list_of_devices
    })
    print(f'Получено {len(list_of_devices)} аппарата(ов)')
    COUNT += 1
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

    for bd_link in bd_links[START:STOP]:
        html = get_request(bd_link['link'])
        if html.status_code != 200:
            print('Ошибка открытия страницы - ', bd_link['link'])
            print(html)
            continue
        BD_KYOCERA.append(get_kyocera_page_content(html.text, bd_link))


def write_kyocera_csv():
    global BD_KYOCERA
    with open('kyocera.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow(['Картридж', 'Тип картриджа', 'Ссылка картриджа', 'Устройства' ])
        for item in BD_KYOCERA:
            devices = str_of_devices(item[0]['devices'])
            for i in item:
                writer.writerow([
                i['brand'],
                i['name'],
                i['type_cart'],
                i['type_cart_rus'],
                i['link'],
                devices
                ])


parse_kyocera()
write_kyocera_csv()


