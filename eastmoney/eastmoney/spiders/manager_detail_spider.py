#基金经理详情页爬虫
import scrapy
import json
import re
import datetime
from bs4 import BeautifulSoup
from eastmoney.spiders.mysql_service import MysqlService


class ManagerDetailSpider(scrapy.Spider):
    name = "manager_detail"

    def start_requests(self):
        url = "http://fund.eastmoney.com/manager/{manager_code}.html"
        while True:
            manage_info = MysqlService().get("blog_fund_manage", ["fund_manager_code"], {"status":1}, True)
            temp_url = url.format(manager_code=manage_info[0])
            yield scrapy.Request(url=temp_url, callback=self.parse)
            
    def parse(self, response):
        body_str = response.body.decode()
        soup = BeautifulSoup(body_str, "lxml")
        manager_code = soup.find("h1", {"id":"jjjl"})["jlid"]
                
        #get fund_info
        pattern = re.compile(r"var mgrlists=(.*?);", re.MULTILINE | re.DOTALL)
        fund_script_str = soup.find("script", text=pattern).string
        fund_json_str = fund_script_str.replace("var mgrlists=", "").replace('valueField', '"valueField"').replace('name','"name"')
        fund_json_str = fund_json_str.replace('type', '"type"').replace("'", '"').replace(";","")
        print(fund_json_str)
        fund_list = json.loads(fund_json_str)
        new_fund_list = []
        for fund_info in fund_list:
            exist_fund_info = MysqlService().get("blog_fund_info", ["fund_code"], {"fund_code":fund_info["valueField"]}, True)
            if exist_fund_info == None:
                fund_data = {"fund_code":fund_info["valueField"], "fund_name":fund_info["name"], "fund_manager_code":manager_code, "status":1}
                fund_data["fund_type"] = int(fund_info["type"])
                new_fund_list.append(fund_data)
        if len(new_fund_list) > 0:
            MysqlService().insert("blog_fund_info", new_fund_list)

        #do manager info update
        start_date_str = soup.find("div", class_="right jd").get_text()
        start_date = re.findall(r"\d{4}-\d{2}-\d{2}", start_date_str)
        fund_assets = soup.find("div", class_="gmleft gmlefts").find("span", class_="numtext").get_text()
        best_return = soup.find("div", class_="gmleft gmlefts").find_next("div").find("span", class_="numtext").get_text()
        best_return = best_return.replace(".","").replace("%","")
        new_manager_str = "--"
        if new_manager_str in best_return:
            manage_info = {"status":3}
        else:
            manage_info = {"best_return":int(best_return), "start_date":start_date[0], "fund_assets":fund_assets, "status":2}
        MysqlService().update("blog_fund_manage", manage_info, {"fund_manager_code":manager_code})
