from bs4 import BeautifulSoup
import csv
import requests
import pickle
import json

URL_KYO = 'http://rashodnika.net/10_1_1.html'  # Kyocera

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}

HOST = 'http://rashodnika.net/'

KYO_CART_PARAM = []

    # 'Ресурс, стр. (5%)', 'Part No.', 'Относительно совместимый тонер:', 'Масса тонера, г.',
    # 'Чип:', 'Заправка картриджа', 'Родственник:', 'Kyocera Parts Lists'


BD_KYOCERA = []

COUNT = 0

START = 0
STOP = 100