from  func import *
# from pprint import pprint

# for brand in ListBrandsFull:  # Проходим по всему списку брендов
# for brand in ListBrands:  # Проходим по подготовленному списку брендов
for brand in ['Panasonic']:  # Проходим по одному бренду
    
    len_brend = 0
    br = cBrand(brand)    # Переменная с ссылками на страницы бренда (или None, если нет такого бренда)

    if br and br[brand]['laser']:
        br['cart_db_las'] = parse(br, 'laser')    # Если ссылка не пустая, запускаем парсинг лазерных картриджей
        len_brend += len(br['cart_db_las'])

    if br and br[brand]['inkjet']:
        br['cart_db_ink'] = parse(br,'inkjet')   # Если ссылка не пустая, запускаем парсинг струйных картриджей
        len_brend += len(br['cart_db_ink'])

    if br and br[brand]['matrix']:
        br['cart_db_matr'] = parse(br,'matrix')   # Если ссылка не пустая, запускаем парсинг матричных картриджей
        len_brend += len(br['cart_db_matr'])


    # print('\n\n')
    # pprint(br, compact=True, sort_dicts=False)
    print(f"Обработан - {brand} - {len_brend} записей")

    if len_brend > 0:
        write_data_to_file_pickle(br, f'{brand}_full_pickle.db')
        write_data_to_file_json(br, f'{brand}_full_json.db')

    del(br)
