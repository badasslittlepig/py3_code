#基金经理的爬虫
import scrapy
import json
import datetime
from eastmoney.spiders.mysql_service import MysqlService 

class ManagerSpider(scrapy.Spider):
    name = "manager"

    def start_requests(self):
        url = 'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=50&sc=abbname&st=asc&pi='
        page_nu = 1
        while page_nu < 51:
            temp_url = url+str(page_nu)
            yield scrapy.Request(url=temp_url, callback=self.parse)
            page_nu += 1

    def parse(self, response):
        body_str = response.body.decode()
        body_str = body_str.replace("var returnjson=", "")
        body_str = body_str.replace("data", '"data"')
        body_str = body_str.replace("record", '"record"')
        body_str = body_str.replace("pages", '"pages"')
        body_str = body_str.replace("curpage", '"curpage"') 
        mysql_con = MysqlService()
        manager_list = json.loads(body_str)
        for manager_info in manager_list["data"]:
            day_ago = (datetime.datetime.now() - datetime.timedelta(days = int(manager_info[6])))
            start_date = day_ago.strftime("%Y-%m-%d")
            manager_data = [{"fund_manager_code":manager_info[0], "fund_manager_name":manager_info[1], "start_date":start_date, "status":1}]
            #mysql_con.insert("blog_fund_manage", manager_data)


