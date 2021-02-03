# -*- coding: utf-8 -*-
#什么值得买搜索列表爬虫
import scrapy
import time
import hashlib
from bs4 import BeautifulSoup
import urllib3
import json
import ssl
from smzdm.spiders.mysql_service import MysqlService

ssl._create_default_https_context = ssl._create_unverified_context
class GoodsInfoSpider(scrapy.Spider):
    name = "smzdm_search"

    def start_requests(self):
        url = "https://search.smzdm.com/?c=home&s={search_key}&order=time&v=b"
        search_goods_list = MysqlService().get("blog_smzdm_search", ["goods_name","key_words"], {"status":1}, False)
        if len(search_goods_list) > 0:
            for search_goods in search_goods_list:
                temp_url = url.format(search_key=search_goods[0])
                add_params = {"search_goods":search_goods[0], "key_words":search_goods[1]}
                yield scrapy.Request(url=temp_url, callback=self.parse, cb_kwargs=add_params)

    def parse(self, response, search_goods, key_words):
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        key_words_list = {}
        if key_words != "":
            key_words_list = json.loads(key_words)
        body_str = response.body.decode()
        soup = BeautifulSoup(body_str, "lxml")
        goods_list = soup.find("ul",{"id":"feed-main-list"}).find_all("li")
        if len(goods_list) > 0:
            for goods_info in goods_list:
                goods_title = goods_info.find("h5",class_="feed-block-title").find_all("a")[0].get("title")
                goods_url = goods_info.find("h5",class_="feed-block-title").find_all("a")[0].get("href")
                goods_price = goods_info.find("h5",class_="feed-block-title").find("div",class_="z-highlight")
                if goods_price == None:
                    continue
                else:
                    goods_price = goods_price.get_text()
                expired_logo = goods_info.find("span", class_="search-pastdue-mark")
                if expired_logo == None:
                    if "key_words" in key_words_list.keys():
                        check_result = self.checkGoodsTitleKeyWords(goods_title, key_words_list)
                    else:
                        check_result = True
                    if check_result == True:
                        unique_str = hashlib.md5()
                        unique_str.update(goods_url.encode("utf-8"))
                        url_md5 = unique_str.hexdigest()
                        exist_condition = {"url_md5":url_md5}
                        exist_goods_info = MysqlService().get("blog_smzdm_search_trace", ["id"], exist_condition, True)
                        goods_save_data = {"url_md5":url_md5, "goods_url":goods_url, "goods_title":goods_title, "goods_price":goods_price}
                        goods_save_data["create_date"] = now_date
                        if exist_goods_info == None:
                            MysqlService().insert("blog_smzdm_search_trace", [goods_save_data])
                            self.noticeWechat(goods_save_data)

    #关键词检测
    @staticmethod
    def checkGoodsTitleKeyWords(goods_title, key_words):
        check_result = True
        for val_str in key_words["key_words"]:
            if val_str in goods_title:
                if key_words["method"] == "or":
                    return True
            else:
                if key_words["method"] == "and":
                    return False
        return check_result
   	 
    #打接口进行微信通知
    @staticmethod
    def noticeWechat(goods_data):
        notice_uri = "http://test.skyshappiness.com/index.php?m=Admin&c=ApiNotice&a=wechatNotice"
        notice_content = "商品标题："+goods_data["goods_title"]+"\r\n"+"商品价格："+goods_data["goods_price"]
        notice_data = {"notice_msg":notice_content, "notice_uri":goods_data["goods_url"]}
        http = urllib3.PoolManager()
        http.request("POST", notice_uri, fields=notice_data)

