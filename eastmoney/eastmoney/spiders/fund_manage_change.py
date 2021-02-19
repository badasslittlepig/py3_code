# -*- coding: utf-8 -*-
#基金经理的爬虫
import scrapy
import json
import datetime
from bs4 import BeautifulSoup
import urllib3
import ssl
from eastmoney.spiders.mysql_service import MysqlService 

class ManagerSpider(scrapy.Spider):
    name = "fund_manager"

    def start_requests(self):
        url = 'http://fund.eastmoney.com/{fund_code}.html?spm=search'
        fund_list = MysqlService().get("blog_fund_own", ["DISTINCT(fund_code), fund_manage_name, fund_manage_code"], {"status":1}, False)
        if len(fund_list) > 0:
            for fund_info in fund_list:
                temp_url = url.format(fund_code=fund_info[0])
                add_params = {"uri":temp_url, "manage_name":fund_info[1]}
                yield scrapy.Request(url=temp_url, callback=self.parse, cb_kwargs=add_params)

    def parse(self, response, uri, manage_name):
        body_str = response.body.decode()
        soup = BeautifulSoup(body_str, "lxml")
        manage_list = soup.find("li",{"id":"fundManagerTab"}).find_all("tr")
        scrap_manage_name = manage_list[1].find("td", class_="td02").get_text()
        if scrap_manage_name != "":
            scrap_manage_name = scrap_manage_name.strip("\n\r    \xa0").replace(' ', "")
        if scrap_manage_name != manage_name:
            notice_str = "基金经理貌似不一致：" + manage_name
            notice_info = {"notice_msg":notice_str, "notice_uri":uri}
            self.noticeWechat(notice_info)

    #打接口进行微信通知
    @staticmethod
    def noticeWechat(notice_data):
        notice_uri = "http://test.skyshappiness.com/index.php?m=Admin&c=ApiNotice&a=noticeSth"
        http = urllib3.PoolManager()
        http.request("POST", notice_uri, fields=notice_data)


