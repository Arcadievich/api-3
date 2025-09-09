import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    method_url = 'https://api.vk.ru/method/utils.getShortLink'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'v': '5.199',
        'url': url,
        'private': '0',
        }
    response = requests.get(method_url, headers=headers, params=payload)
    response.raise_for_status()
    short_link = response.json()
    return short_link['response']['short_url']


def count_clicks(token, key):
    method_url = 'https://api.vk.ru/method/utils.getLinkStats'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'v': '5.199',
        'key': key,
        'interval': 'forever',
        'extended': '0',
        }
    response = requests.get(method_url, headers=headers, params=payload)
    response.raise_for_status()
    url_clicks = response.json()
    print(url_clicks)
    return url_clicks['response']['stats'][0]['views']


def is_not_shorten_link(token, url):
    method_url = 'https://api.vk.ru/method/utils.getLinkStats'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'v': '5.199',
        'key': url,
        'interval': 'forever',
        'extended': '0',
        }
    response = requests.get(method_url, headers=headers, params=payload)
    response.raise_for_status()
    url_clicks = response.json()
    return 'error' in url_clicks

def main():
    load_dotenv()
    token = os.environ['API_KEY_VK']

    parser = argparse.ArgumentParser(
        description='Получение кол-ва переходов по ссылке\сокращенной ссылки'
    )

    parser.add_argument('link', help='Ссылка для проверки')
    args = parser.parse_args()
    user_url = args.link
    parsed_user_url = urlparse(user_url)

    if is_not_shorten_link(token, parsed_user_url.path.removeprefix('/')):
        try:
            short_link = shorten_link(token, user_url)
            print(f'Сокращенная ссылка: {short_link}')
        except KeyError:
            print('Некорректно указана ссылка')
    else:
        try:
            print('Переходы по ссылке: ',
                  count_clicks(token, parsed_user_url.path.removeprefix('/')))
        except KeyError:
            print('Некорректно указана ссылка')


if __name__ == '__main__':
    main()