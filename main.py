import json
import os
import requests
import pyrominfo.pyrominfo.snes as snes


def snes_info(filename):
    snes_parser = snes.SNESParser()
    props = snes_parser.parse(filename)
    if props:
        print(f'{props["title"]}')
        print(f'{props["region"]}')
    return props['title']


def get_console(argument):
    switcher = {
        'sfc': 'SNES',
        'smc': 'SNES',
        'md':'',
        'bin': '',
        'gb': 'GB',
        'gbc': 'GBC',
        'nes': 'NES',
    }
    return switcher.get(argument)


def giant_bomb_request(title, api_key):
    headers = {'User-Agent': 'gripper'}
    params = {
        'resources': 'game',
        'query': title,
        'api_key': api_key,
        'format': 'json'
    }
    response = requests.get(url='http://www.giantbomb.com/api/search/', headers=headers, params=params)
    return json.loads(response.text)


def print_game_name():
    path = '/media/mugenoesis/RETRODE'
    api_key = '287231aaca973206a0fbdd3086c1ead394bd99cc'
    files = os.listdir(path)
    files.remove('RETRODE.CFG')
    breakout = False
    console = get_console(files[0].split('.')[-1])
    print(console)
    print(files)
    filename = f'{path}/{files[0]}'
    if console == 'SNES':
        title = snes_info(filename)
        search_results = giant_bomb_request(title, api_key)
        for results in search_results['results']:
            if breakout is True:
                break
            aliases = str(results.get('aliases')).lower().splitlines()
            if title.lower() in aliases or title.lower() == results['name']:
                for platform in results['platforms']:
                    if platform['abbreviation'] == 'SNES':
                        print('valid')
                        breakout = True
                        break


if __name__ == '__main__':
    print_game_name()