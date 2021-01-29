#基金爬虫
import scrapy
import json
import datetime
import re
from bs4 import BeautifulSoup
from eastmoney.spiders.mysql_service import MysqlService

class ManagerSpider(scrapy.Spider):
    name = "fund"

    def start_requests(self):
        url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={fund_code}&topline=10&year=&month=&rt=0.6134177124013891"
        while True:
            fund_info = MysqlService().get("blog_fund_info", ["fund_code"], {"status":1}, True)
            temp_url = url.format(fund_code=fund_info[0])
            add_params = {"fund_code":fund_info[0]}
            yield scrapy.Request(url=temp_url, callback=self.fundStockInfo, cb_kwargs=add_params)

    def parse(self, response):
        body_str = response.body.decode()
        soup = BeautifulSoup(body_str, "lxml")
        fund_code = soup.find("span", class_="fix_fcode").get_text()
        unuse_str = "--"
        #fund return list
        #dom one one_month_return
        new_establish_fund = soup.find("div",class_="xinfajj")
        if new_establish_fund == None:
            one_month_return = soup.find("span",text=re.compile("近1月")).find_next_sibling("span").get_text()
            if (unuse_str in one_month_return) == False:
                one_month_return = one_month_return.replace("近1月：","").replace(".","").replace("%","")
            else:
                one_month_return = 0
            #one_year_return
            one_year_return = soup.find("span",text=re.compile("近1年")).find_next_sibling("span").get_text()
            if (unuse_str in one_year_return) == False:
                one_year_return = one_year_return.replace("近1年：","").replace(".","").replace("%","")
            else:
                one_year_return = 0
            #dom two three_month_return
            three_month_return = soup.find("span",text=re.compile("近3月")).find_next_sibling("span").get_text()
            if (unuse_str in three_month_return) == False:
                three_month_return = three_month_return.replace("近3月：","").replace(".","").replace("%","")
            else:
                three_month_return = 0
            #three_year_return
            three_year_return = soup.find("span",text=re.compile("近3年")).find_next_sibling("span").get_text()
            if (unuse_str in three_year_return) == False:
                three_year_return = three_year_return.replace("近3年：","").replace(".","").replace("%","")
            else:
                three_year_return = 0
            #dom three six_month_return
            six_month_return = soup.find("span",text=re.compile("近6月")).find_next_sibling("span").get_text()
            if (unuse_str in six_month_return) == False:
                six_month_return = six_month_return.replace("近6月：","").replace(".","").replace("%","")
            else:
                six_month_return = 0
            #return since establishment
            total_return = soup.find("span",text=re.compile("成立来")).find_next_sibling("span").get_text()
            if (unuse_str in total_return) == False:
                total_return = total_return.replace("成立来：","").replace(".","").replace("%","")
            else:
                total_return = 0
            
            #fund info list
            fund_info_list = soup.find("div", class_="infoOfFund").find("table").find_all("td")
            fund_assets = fund_info_list[1].get_text().replace("基金规模：","")
            fund_assets = fund_assets.split("（")[0]
            fund_establish_date = fund_info_list[3].get_text().replace("成 立 日：","")
            fund_level = fund_info_list[5].get_text().replace("基金评级：","")

            
            save_fund_info = {"one_month_return":int(one_month_return),"three_month_return":int(three_month_return),"six_month_return":int(six_month_return)}
            save_fund_info["one_year_return"] = int(one_year_return)
            save_fund_info["three_year_return"] = int(three_year_return)
            save_fund_info["total_return"] = int(total_return)
            if (unuse_str in fund_establish_date) == False:
                save_fund_info["start_date"] = fund_establish_date
            save_fund_info["fund_level"] = fund_level
            save_fund_info["fund_assets"] = fund_assets
            save_fund_info["status"] = 2
        else:
            save_fund_info = {"status":2}
        MysqlService().update("blog_fund_info", save_fund_info, {"fund_code":fund_code})


    #基金持仓详情页抓取
    def fundStockInfo(self, response, fund_code):
        body_str = response.body.decode()
        json_str = body_str.replace("var apidata=","").replace(";","").replace("content",'"content"').replace("arryear",'"arryear"').replace("curyear",'"curyear"')
        fund_stock_return = json.loads(json_str)
        if fund_stock_return["content"] != "":
            soup = BeautifulSoup(fund_stock_return["content"], "lxml")
            stock_list = soup.find_all("div", class_="box")
            save_stock_list = []
            for stock_info in stock_list:
                report_date = stock_info.find("h4",class_="t").find("label", class_="right").find("font",class_="px12").get_text()
                hold_stock_list = stock_info.find("table").find("tbody").find_all("tr")
                for hold_stock_info_str in hold_stock_list:
                    hold_stock_info_list = hold_stock_info_str.find_all("td")
                    stock_code = hold_stock_info_list[1].get_text()
                    stock_name = hold_stock_info_list[2].get_text()
                    stock_assets = int(hold_stock_info_list[-1].get_text().replace(",","").replace(".",""))
                    exist_condition = {"fund_code":fund_code,"stock_code":stock_code,"statistics_date":report_date}
                    exist_fund_info = MysqlService().get("blog_fund_stock", ["id"], exist_condition, True)
                    if exist_fund_info == None:
                        temp_data = {"stock_code":stock_code, "stock_name":stock_name, "stock_assets":stock_assets,"statistics_date":report_date}
                        temp_data["fund_code"] = fund_code
                        save_stock_list.append(temp_data)
            if len(save_stock_list) > 0:
                MysqlService().insert("blog_fund_stock", save_stock_list)

        #基金基础信息获取
        url = "http://fund.eastmoney.com/{fund_code}.html"
        temp_url = url.format(fund_code=fund_code)
        yield scrapy.Request(url=temp_url, callback=self.parse)



