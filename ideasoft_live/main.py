import time

import requests

ENDPOINT = 'https://canli.ideasoft.com.tr/api/v1/live/export.php'
items = []
refreshed = False


def decode(obj):
    return f'{obj["city"]}/{obj["county"]}, {obj["price"]}\n{obj["quantity"]}, {obj["name"]}\n---'


def print_items(response):
    for sale in response['sales']:
        if sale['id'] not in items:
            items.append(sale['id'])
            print(decode(sale))


def perform():
    with requests.Session() as session:
        while True:
            response = session.get(ENDPOINT).json()
            print_items(response)
            time.sleep(1)


def main():
    try:
        perform()
    except KeyboardInterrupt:
        print('\rExiting')
