#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

from ast import NotIn
from asyncore import write
from datetime import datetime
import os
import requests

mediaContent = []
file_path = os.path.dirname(__file__)

download_domain = 'https://1253731777.vod2.myqcloud.com/cd68bb45vodbj1253731777/e5247e38387702305075889524/'

def start():
    temp_file_name = datetime.now().strftime("%Y%m%d%H%M%S") + "_temp.mp4"
    with open(os.path.join(file_path, 'playlist_eof.m3u8'), encoding='UTF-8') as lines:
        for line in lines:
            if line.startswith("#") == False :
                print(line)
                download_uri = download_domain + line
                media_content = requests.get(url=download_uri).content
                with open(temp_file_name, mode='ab') as f:
                    f.write(media_content)
                    f.close()
    exit()
if __name__ == '__main__':
    start()
