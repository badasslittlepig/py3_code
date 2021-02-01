# -*- coding: utf-8 -*-
#基金爬虫
import scrapy
import json
import time 
import re
import hashlib
from bs4 import BeautifulSoup
from yicai.spiders.mysql_service import MysqlService

class ManagerSpider(scrapy.Spider):
    name = "yicai_epaper"

    def start_requests(self):
        url = "https://www.yicai.com/epaper/pc/{year_month}/{day_nu}/node_A{page_nu}.html"
        year_month = time.strftime("%Y%m", time.localtime())
        day_nu = time.strftime("%d", time.localtime())
        start_page = 1
        while start_page < 13:
            if start_page < 10:
                page_nu = "0"+str(start_page)
            else:
                page_nu = str(start_page)
            temp_url = url.format(year_month=year_month, day_nu=day_nu, page_nu=page_nu)
            yield scrapy.Request(url=temp_url, callback=self.parse)
            start_page = start_page+1

    def parse(self, response):
        if response.status == 200:
            now_date = time.strftime("%Y-%m-%d", time.localtime())
            body_str = response.body.decode()
            soup = BeautifulSoup(body_str, "lxml")
            news_list = soup.find("div",class_="newslist").find("ul").find_all("li")
            save_news_list = []
            for news_info in news_list:
                news_uri = news_info.find("a").get("href")
                news_title = news_info.find("a").get_text()
                news_desc = news_info.find_all("p")[1].get_text()
                unique_str = hashlib.md5()
                unique_str.update(news_uri.encode("utf-8"))
                news_md5_str = unique_str.hexdigest()
                exist_condition = {"news_md5":news_md5_str}
                exist_news_info = MysqlService().get("blog_fund_news", ["id"], exist_condition, True)
                if exist_news_info == None:
                    save_news_data = {"news_url":news_uri, "news_title":news_title, "news_from":"第一财经", "creat_date":now_date}
                    save_news_data["news_md5"] = news_md5_str
                    save_news_data["news_desc"] = news_desc.strip()
                    save_news_list.append(save_news_data)
            if len(save_news_list) > 0:
                MysqlService().insert("blog_fund_news", save_news_list)
