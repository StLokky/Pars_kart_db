from common_func import *

data1 = read_kyocera_pickle('pickle_kyo.bd')
for d in data1:
    print(d, end="\n\n")

print("************************************************************************", end="\n\n")
data2 = read_kyocera_json('json_kyo_bd.txt')
for d in data2:
    print(d, end="\n\n")