#基金经理的爬虫

import scrapy
import json
import mysql_service

class ManagerSpider(scrapy.Spider):
    name = "manager"

    def start_requests(self):
        urls = [
            'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=50&pi=1&sc=abbname&st=asc'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        body_str = response.body.decode()
        body_str = body_str.replace("var returnjson=", "")
        body_str = body_str.replace("data", '"data"')
        body_str = body_str.replace("record", '"record"')
        body_str = body_str.replace("pages", '"pages"')
        body_str = body_str.replace("curpage", '"curpage"') 
        manager_list = json.loads(body_str)
        for manager_info in manager_list["data"]:
            manager_data = {"manager_code":manager_info[0], "manager_name":manager_info[1]}
            mysql_service.insert(mysqlConf,"blog_fund_manage", manager_data)
            fund_code_list = manager_info[4].split(",")
            fund_name_list = manager_info[5].split(",")
            for (key,fund_code) in enumerate(fund_code_list):
                fund_data = {"manager_name":manager_info[0],"fund_code":fund_code, "fund_name":fund_name_list[key]}


