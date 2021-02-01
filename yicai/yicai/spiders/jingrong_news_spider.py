# -*- coding: utf-8 -*-
#第一财经金融新闻爬虫
import scrapy
import json
import time 
import re
import hashlib
from bs4 import BeautifulSoup
from yicai.spiders.mysql_service import MysqlService

class ManagerSpider(scrapy.Spider):
    name = "yicai_jinrong"

    def start_requests(self):
        url = "https://www.yicai.com/news/jinrong/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            now_date = time.strftime("%Y-%m-%d", time.localtime())
            body_str = response.body.decode()
            soup = BeautifulSoup(body_str, "lxml")
            news_list = soup.find("div",{"id":"newslist"}).find_all("a")
            save_news_list = []
            for news_info in news_list:
                news_uri = news_info.get("href")
                if news_uri != "":
                    news_uri = "https://www.yicai.com" + news_uri
                news_title = news_info.find("h2").get_text()
                news_desc = news_info.find("p").get_text()
                unique_str = hashlib.md5()
                unique_str.update(news_uri.encode("utf-8"))
                news_md5_str = unique_str.hexdigest()
                exist_condition = {"news_md5":news_md5_str}
                exist_news_info = MysqlService().get("blog_fund_news", ["id"], exist_condition, True)
                if exist_news_info == None:
                    save_news_data = {"news_url":news_uri, "news_title":news_title, "news_from":"第一财经金融", "creat_date":now_date}
                    save_news_data["news_md5"] = news_md5_str
                    save_news_data["news_desc"] = news_desc.strip()
                    save_news_list.append(save_news_data)
            if len(save_news_list) > 0:
                MysqlService().insert("blog_fund_news", save_news_list)
