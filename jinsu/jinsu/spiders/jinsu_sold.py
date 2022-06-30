import json
import re
import scrapy
import urllib.parse
import urllib3
from bs4 import BeautifulSoup


class JinsuSoldSpider(scrapy.Spider):
    name              = 'jinsu_sold'
    allowed_domains   = ['bbs.527moto.com']
    start_urls        = ['https://bbs.527moto.com/forum.php?mod=forumdisplay&fid=12&filter=author&orderby=dateline']
    unneed_sold_user  = ["沪牌超市薛老板", "聚友机车俱乐部", "上海满昌修理部", "禾清机车龍老板", "雷霆车行年糕", "聚摩club渣老板", "Zmotor-大卫", "上海倪氏",
     "零柒机车_小勇", "奔达4S店", "啊电单车", "杨浦_ZMotor小小", "熊猫机9988", "口水娃", "浦江镇沪摩机车", "欣亦机车-小黑皮", "杨浦摩驿机车", "聚摩CLUB小宁-Inking", "景泰车行白老板",
     "小谢", "上海苑乐", "闵行聚友二手车", "上海驾驭机车", "聚摩club-77", "雷霆车行牛老板", "上海ZMOTOR烨", "擎天机车", "聚摩club塔塔", "驾驭机车-熊", "麒麟机车俱乐部", "驾驭机车—A.M.G",
     "上海魔域纹身", "骑麟机车俱乐部", "骑迹SMKClub", "琦鲁MOTO高桥店", "上海明帆", "鼎骑酒桶", "杨浦-ZMotor石头", "夏日车业", "阿东车行", "9MT-ALEN", "丰庄逸捷梁氏车行", "丰庄逸捷",
     "杨浦Zmotor啊罡", "上海酷雷机车", "品道车业小欧", "51RT车尊技研", "9MT-啊喆", "K1摩托租赁", "品道车业小欧", "OMC摩托车俱乐部", "华兴机车", "BG4CKZ阿杰"]
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
            post_data = { "acticle_title": sold_title, "grab_uri" : sold_uri, "is_grabed" : 1, "author": sold_user}
            notice_grab_uri_result = self.request_pool.request("POST", self.grab_notice_uri, post_data)
            return_str = notice_grab_uri_result.data.decode("UTF-8")
            return_data = json.loads(return_str)
            if return_data["status"] == 200 :
                wechat_notice_data = {"notice_msg":sold_title, "notice_uri": sold_uri, "notice_user":"ok_Tas4xrdDs5sf_A1mrr29MTtUY,ok_Tas7S8rDGbcYce8u97I6g7HK8,ok_TaswRfYvH3dCQRgMd34JrRgTw"}
                self.request_pool.request("POST", self.wechat_notice_uri, wechat_notice_data)