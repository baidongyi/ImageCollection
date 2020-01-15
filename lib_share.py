from urllib import request
from bs4 import BeautifulSoup
import requests
import os
import datetime
import ssl
import sys


def wl(msg: str, level: int = 1):
    show_level = 1
    if level <= show_level:
        assert isinstance(msg, str)
        print(msg)


def get_base_folder() -> str:
    if sys.platform == 'linux':
        base_folder = '~/Pic18'
    elif sys.platform == 'darwin':
        base_folder = '~/Pic18'
    elif sys.platform == 'win32':
        base_folder = r'C:\Pic18'
    return base_folder


def get_uni_file_path(folder: str, img_web: str, img_id: str, img_num: str) -> str:
    return folder + '\\' + img_web + '_' + str(img_id) + '_' + str(img_num) + '.jpg'


def rename_temp(temp_folder: str):
    file_list = os.listdir(temp_folder)
    if len(file_list) > 700:
        os.rename(temp_folder, temp_folder + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
        os.mkdir(temp_folder)


# 0 for downloaded successfully , 1 for already exists, 2 for error 404 not found
def save_image_by_url_to_file(file_path: str, url: str, ref_url: str = 'null') -> int:
    if os.path.exists(file_path):
        #wl('File Already Exists:' + file_path, 1)
        return 1

    if ref_url == 'null':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/62.0.3202.94 Safari/537.36'}
    else:
        headers = {"Referer": ref_url,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/62.0.3202.94 Safari/537.36'}

    content = requests.get(url, headers=headers)
    if content.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in content:
                f.write(chunk)
        wl('M2: Save File: ' + file_path, 1)
        return 0
    else:
        return 2


def get_soup_by_url(url) -> object:
    wl('try load url =>' + url, 3)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    context = ssl._create_unverified_context()
    page_info = request.urlopen(page, context=context).read()
    return BeautifulSoup(page_info, 'html.parser')  # 'lxml'


def is_img_url_valid(url: str):
    wl('try url ->' + url, 3)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/62.0.3202.94 Safari/537.36'}
    content = requests.get(url, headers=headers)
    if content.status_code == 200:
        return True
    else:
        return False
