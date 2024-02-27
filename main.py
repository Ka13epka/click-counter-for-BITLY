import os
import requests
from urllib.parse import urlparse
import argparse



def shorten_link(token, long_url):
    bit_url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {
        'long_url': long_url,
    }
    headers = {
        'Authorization': f'Bearer {token}',
    }
  
    response = requests.post(bit_url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    bit_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        "unit": "month",
        "units": "-1"
    }
    
    response = requests.get(bit_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(token, url):
    bit_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(bit_url, headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(description='Автогенератор ссылок битли, и проверка сколько человек на неё зашли')
    parser.add_argument('url', help='link')
    args = parser.parse_args()
    url = args.url
    token = os.getenv('APIKEY_BITLY')
    parsed_url = urlparse(url)
    combined_path = f'{parsed_url.netloc}{parsed_url.path}'
    try:
        if is_bitlink(token, combined_path):
            print(count_clicks(token, combined_path))
        else:
            print(shorten_link(token, url))    
    except requests.exceptions.HTTPError as error:
        print(f'Неправильная ссылка: {error}')
    

if __name__ == "__main__":
    main()