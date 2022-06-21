#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

from ast import NotIn
from asyncore import write
import os
import json
import re
import ssl
import time
import requests
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

file_path = os.path.dirname(__file__)
with open(os.path.join(file_path, 'config.json'), encoding='UTF-8') as fp:
    CONFIG = json.load(fp)

tik_tok_prefix_url = 'https://www.douyin.com/user/'

file_save_path = file_path + r'/spider/'

# display = Display(visible=0, size=(1920, 1080))
# display.start()


# http://chromedriver.storage.googleapis.com/index.html
chrome_driver_path = file_path + '/chromedriver'
service = Service(executable_path=chrome_driver_path)
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.maximize_window()


ssl._create_default_https_context = ssl._create_unverified_context
def start():
    try:
        for tik_tok_id in CONFIG['tik_tok_id_list']:
            req_url = tik_tok_prefix_url + tik_tok_id
            browser.get(req_url)
            browser.implicitly_wait(10)
            browser.get(browser.current_url)
            handle_page_lazy_loading()
            # save_userinfo()
            save_works()
    finally:
        browser.close()
        browser.quit()
        # display.stop()


def handle_page_lazy_loading():
    window_height = [browser.execute_script('return document.body.scrollHeight;')]
    while True:
        browser.execute_script('scroll(0,100000)')
        time.sleep(3)
        half_height = int(window_height[-1]) / 2
        browser.execute_script('scroll(0,{0})'.format(half_height))
        browser.execute_script('scroll(0,100000)')
        time.sleep(3)
        check_height = browser.execute_script('return document.body.scrollHeight;')
        if check_height == window_height[-1]:
            break
        else:
            window_height.append(check_height)


def save_userinfo():
    username = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/div[1]/div[2]/h1/span/span/span/span/span').text
    if username == "":
        username = browser.find_element(By.CLASS_NAME, "OKOabD2C").find_element(By.TAG_NAME, "span").text
    filepath = file_save_path + username
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    os.chdir(filepath)
    file_name = '主页信息.txt'
    with open(file_name, 'a+', encoding='UTF-8') as file:
        file.write(browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/div[1]').text)
        file.close()


def save_works():
    user_name = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/div[1]/div[2]/h1/span/span/span/span/span').text
    if user_name == "":
       user_name = browser.find_element(By.CLASS_NAME, "Yja39qrE").find_element(By.CLASS_NAME, "Nu66P_ba").text
    save_dir = file_save_path + user_name
    grabed_file_name = '已爬取.txt'
    ul =  browser.find_element(By.CLASS_NAME, 'ARNw21RN')
    lis = ul.find_elements(By.XPATH,"li")
    li_len = len(lis)
    i = 0
    while i < li_len:
        try:
            grabed_content_list = []
            forward_element = lis[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
            video_id = forward_element.split('/')[-1]
            video_id = video_id.split('?')[0]
            log_file = save_dir + r"/" + grabed_file_name
            if os.path.exists(log_file):
                grabed_file_handle = open(log_file, 'r', encoding='UTF-8')
                grabed_content_list = grabed_file_handle.read().split(";")
                grabed_file_handle.close()
            if video_id not in grabed_content_list:
                print(video_id)
                browser.execute_script("window.open('','_blank');")
                browser.switch_to.window(browser.window_handles[1])
                browser.get(forward_element)
                html_source = browser.page_source
                title = browser.find_element(By.CLASS_NAME, "z8_VexPf").text
                title_res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
                title = title_res.sub("", title)
                download_uri = re.findall('playAddr%22%3A%5B%7B%22src%22(.*?)%3F', html_source)[1]
                video_uri = requests.utils.unquote(download_uri).replace(':"', 'https:')
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                os.chdir(save_dir)
                video_content = requests.get(url=video_uri).content
                with open(title + "_" + video_id + '.mp4', mode='wb') as f:
                    f.write(video_content)
                    f.close()
                grabed_file_handle = open(log_file, 'a+', encoding='UTF-8')
                grabed_file_handle.write(video_id + ";")
                grabed_file_handle.close()
                
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
        except Exception as e:
            print(e.args)
            print(str(e))
            # print(browser.page_source)
            exit()
            # continue

        i = i + 1
        if i % 10 == 0:
            time.sleep(3)


if __name__ == '__main__':
    start()
