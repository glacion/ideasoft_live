import time

import requests

# TODO: This will leak memory.
items = []


def parse(obj):
    return f'{obj["city"]}, {obj["price"]}, {obj["quantity"]}\n\thttps:{obj["image"]}\n\t{obj["name"]}\n---'


def csv(sale):
    return f'{sale["id"]},{sale["city"]},{sale["name"]},{sale["price"]},{sale["image"]},{sale["quantity"]},{sale["time"]}'


def print_items(response, args):
    for sale in response['sales']:
        if sale['id'] not in items:
            items.append(sale['id'])
            if args.csv:
                print(csv(sale))
            else:
                print(parse(sale))


def perform(args):
    params = {'refreshed': False}
    with requests.Session() as session:
        while True:
            response = session.get(args.endpoint).json()
            print_items(response, args)
            time.sleep(args.interval)


def create_parser():
    import argparse
    parser = argparse.ArgumentParser(
        prog='ideasoft_live', description='Polls sale data published by ideasoft.')
    parser.add_argument(
        '--csv', help='print sales as csv lines.', action='store_true')
    parser.add_argument('--interval', default=1, type=int,
                        help='time between the calls to server.')
    parser.add_argument(
        '--endpoint', default='https://canli.ideasoft.com.tr/api/v1/live/export.php', help='API endpoint to poll.')
    return parser


def main():
    try:
        parser = create_parser()
        args = parser.parse_args()
        perform(args)
    except KeyboardInterrupt:
        print('\rExiting')


if __name__ == '__main__':
    main()
