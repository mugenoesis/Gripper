import json
import os
import requests
import pyrominfo.pyrominfo.snes as snes
from shutil import copy


def snes_info(filename):
    snes_parser = snes.SNESParser()
    props = snes_parser.parse(filename)
    if props:
        print(f'{props["title"]}')
        print(f'{props["region"]}')
    return props


def get_console(argument):
    switcher = {
        'sfc': 'SNES',
        'smc': 'SNES',
        'md': '',
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


def rip_game():
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
        rom_info = snes_info(filename)
        title = rom_info["title"]
        search_results = giant_bomb_request(title, api_key)
        for results in search_results['results']:
            if breakout is True:
                break
            aliases = str(results.get('aliases')).lower().splitlines()
            if title.lower() in aliases or title.lower() == results['name']:
                for platform in results['platforms']:
                    if platform['abbreviation'] == 'SNES':
                        print('valid')
                        if not os.path.exists(f'./{title}'):
                            os.mkdir(f'./{title} - {rom_info["region"]}')
                        for file in files:
                            destination_file = f'./{title} - {rom_info["region"]}/{title}.{file.split(".")[-1]}'
                            if not os.path.exists(destination_file):
                                copy(filename, destination_file)
                        breakout = True
                        break


if __name__ == '__main__':
    rip_game()
