import json
import re
import scrapy
import urllib.parse
import urllib3
from bs4 import BeautifulSoup


class JinsuSoldSpider(scrapy.Spider):
    name              = 'jinsu_sold'
    allowed_domains   = ['bbs.527moto.com']
    start_urls        = ['https://bbs.527moto.com/forum-12-1.html']
    unneed_sold_user  = ["沪牌超市薛老板"]
    wechat_notice_uri = "http://test.skyshappiness.com/index.php?m=Admin&c=ApiNotice&a=noticeSth"
    grab_notice_uri   = "http://test.skyshappiness.com/index.php?m=Open&c=Grab&a=grabUriAdd"
    request_pool      = urllib3.PoolManager()

    def parse(self, response):
        host_info = urllib.parse.urlparse(self.start_urls[0])
        body_str = response.body.decode("gbk")
        soup = BeautifulSoup(body_str, "lxml")
        sold_list = soup.find_all("tbody", id=re.compile("normalthread_"))
        for sold_info in sold_list:
            sold_title      = sold_info.find("th", class_="new").find("a", class_="xst").string
            sold_uri_detail = sold_info.find("th", class_="new").find("a", class_="xst").get("href")
            sold_user       = sold_info.find("td", class_="by").find("cite").find("a").string
            if sold_user in self.unneed_sold_user :
                continue
            sold_uri = host_info.scheme + "://" + host_info.netloc + "/" + sold_uri_detail
            post_data = { "acticle_title": sold_title, "grab_uri" : sold_uri, "is_grabed" : 1 }
            notice_grab_uri_result = self.request_pool.request("POST", self.grab_notice_uri, post_data)
            return_str = notice_grab_uri_result.data.decode("UTF-8")
            return_data = json.loads(return_str)
            if return_data["status"] == 200 :
                wechat_notice_data = {"notice_msg":sold_title, "notice_uri": sold_uri}
                self.request_pool.request("POST", self.wechat_notice_uri, wechat_notice_data)
