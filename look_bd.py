import pickle
import json
import pprint

def write_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow(['Картридж', 'Тип картриджа', 'Ссылка картриджа', 'Устройства' ])
        for item in data:
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
    return 0


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


def read_data_from_file_pickle(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
    except Exception as e:
        return None
    return data


def read_data_from_file_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except Exception as e:
        return None
    return data


data1 = read_data_from_file_pickle('pickle_kyo.bd')
for d in data1:
    print(d, end="\n\n")

print("************************************************", end="\n\n")
data2 = read_data_from_file_json('json_kyo_bd.txt')
for d in data2:
    print(d, end="\n\n")
