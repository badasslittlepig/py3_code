import json
import re
import scrapy
import urllib.parse
import urllib3
from bs4 import BeautifulSoup


class JinsuSoldSpider(scrapy.Spider):
    name                = 'jinsu_detail'
    allowed_domains     = ['bbs.527moto.com']
    request_pool        = urllib3.PoolManager()
    get_grab_uri        = "https://www.skyshappiness.com/index.php?m=Open&c=BbsDetail&a=getList"
    start_urls_response = request_pool.request("POST", get_grab_uri)
    return_str = start_urls_response.data.decode("UTF-8")
    print(return_str)

    wechat_notice_uri = "http://www.skyshappiness.com/index.php?m=Admin&c=ApiNotice&a=noticeSth"
    grab_notice_uri   = "http://www.skyshappiness.com/index.php?m=Open&c=Grab&a=grabUriAdd"

    def parse(self, response):
        print(self.start_urls_response)
        print(11111)
        exit(11);
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
            post_data = { "acticle_title": sold_title, "grab_uri" : sold_uri, "is_grabed" : 1, "author": sold_user}
            notice_grab_uri_result = self.request_pool.request("POST", self.grab_notice_uri, post_data)
            return_str = notice_grab_uri_result.data.decode("UTF-8")
            return_data = json.loads(return_str)
            if return_data["status"] == 200 :
                sold_title = sold_title + "\r\nnlp分词结果：" + return_data["data"]["nlp_name"];
                wechat_notice_data = {"notice_msg":sold_title, "notice_uri": sold_uri, "notice_user":"ok_Tas4xrdDs5sf_A1mrr29MTtUY,ok_Tas7S8rDGbcYce8u97I6g7HK8,ok_TaswRfYvH3dCQRgMd34JrRgTw"}
                self.request_pool.request("POST", self.wechat_notice_uri, wechat_notice_data)