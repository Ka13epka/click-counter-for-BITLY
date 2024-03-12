import os
from urllib.parse import urlparse
import argparse
import requests
from dotenv import load_dotenv


def shorten_link(headers, url):
    bit_url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {
        'long_url': url,
    }

    response = requests.post(bit_url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(headers, bitlink):
    url_sum = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'

    params = {
        "unit": "month",
        "units": "-1"
    }
    
    response = requests.get(url_sum, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(headers, url):
    bit_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'

    response = requests.get(bit_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    headers = {
        "Authorization": f"Bearer {bitly_token}",
    }
    parser = argparse.ArgumentParser(description='Сокращает ссылки и выводит количество переходов по ней')
    parser.add_argument('link', help='Введите ссылку:')
    args = parser.parse_args()
    print(args.link)

    parse_link = urlparse(args.link)
    my_bitlink = f'{parse_link.netloc}{parse_link.path}'
    try:
        if is_bitlink(headers, my_bitlink):
            print(count_clicks(headers, my_bitlink))
        else:
            print(shorten_link(headers, args.link))    
    except requests.exceptions.HTTPError as error:
        print(f'Неправильная ссылка: {error}')
    

if __name__ == "__main__":
    main()