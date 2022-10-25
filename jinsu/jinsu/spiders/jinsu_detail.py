import json
import re
import scrapy
import urllib.parse
import urllib3
from bs4 import BeautifulSoup


class JinsuDetailSpider(scrapy.Spider):
    name              = 'jinsu_detail'
    allowed_domains   = ['bbs.527moto.com']
    request_pool      = urllib3.PoolManager()
    get_grab_uri      = "https://www.skyshappiness.com/index.php?m=Open&c=BbsDetail&a=getList"
    save_data_uri     = "https://www.skyshappiness.com/index.php?m=Open&c=BbsDetail&a=updateInfo"

    def start_requests(self):
        start_urls_response = self.request_pool.request("POST", self.get_grab_uri, {})
        start_urls_str = start_urls_response.data.decode("UTF-8")
        start_urls = json.loads(start_urls_str)
        if start_urls["status"] != 200:
            print("获取帖子爬取列表失败：" + start_urls["msg"])
        for uri_info in start_urls["data"]:
            trans_val = {"id":uri_info["id"], "md5_uri":uri_info["md5_uri"]}
            yield scrapy.Request(url=uri_info["grab_uri"], callback=self.parse, cb_kwargs=trans_val)



    def parse(self, response, id, md5_uri):
        body_str = response.body.decode("gbk")
        soup = BeautifulSoup(body_str, "lxml")
        reply_list_dom = soup.find_all("table", class_="plhin")
        if len(reply_list_dom) > 1:
            reply_name = reply_list_dom[1].find_all("div", class_="authi")[0].find("a").string
            reply_floor = reply_list_dom[1].find("td", class_="plc").find("div", class_="pi").find("a").text
            save_data = {"id":id, "md5_uri":md5_uri, "last_reply_name":reply_name, "last_grap_detail":reply_floor}
            self.request_pool.request("POST", self.save_data_uri, save_data)

