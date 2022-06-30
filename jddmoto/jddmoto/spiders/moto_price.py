import json
import random
import scrapy
import time
import urllib.parse
import urllib3
from bs4 import BeautifulSoup

class MotoPriceSpider(scrapy.Spider):
    name             = 'moto_price'
    allowed_domains  = ['www.jddmoto.com']
    start_urls       = ['https://www.jddmoto.com/ShangHaiShi/used-car/list/{page_no}-2-0-0-0-0-0-2-0-0-0-0-0.html']
    grab_notice_moto = "http://test.skyshappiness.com/index.php?m=Open&c=JddMotoGrab&a=usedMotoAdd"
    request_pool    = urllib3.PoolManager()

    def start_requests(self):
        page_nu = "1"
        temp_url = self.start_urls[0].format(page_no=page_nu)
        yield scrapy.Request(url=temp_url, callback=self.parse, cb_kwargs={"page_nu":page_nu})

    def parse(self, response, page_nu):
        host_info = urllib.parse.urlparse(self.start_urls[0])
        body_str = response.body.decode()
        soup = BeautifulSoup(body_str, "lxml")
        sold_list_dom = soup.find("div", class_="SecondGoods__ListWrapper-sc-1794aar-5").find_all("div", class_="list-item")
        post_list = [];
        for sold_info_dom in sold_list_dom :
            temp_title_span_list = sold_info_dom.find("div", class_="l-title").find_all("span")
            temp_moto_get_license_year = sold_info_dom.find("div", class_="l-tags").find_all("span")[0].get_text()
            temp_moto_price = sold_info_dom.find("div", class_="l-bottom").find("span", class_="price").get_text()
            temp_moto_mile = sold_info_dom.find("div", class_="l-tags").find_all("span")[1].get_text()
            temp_data = {
                "detail_uri" :            host_info.scheme + "://" + host_info.netloc + "/" + sold_info_dom.find("a").get("href"),
                "moto_name" :             temp_title_span_list[0].get_text(),
                "moto_year" :             "",
                "moto_get_license_year" : temp_moto_get_license_year.replace("/", "").strip(),
                "moto_mile" :             temp_moto_mile.replace("/", "").strip(),
                "moto_license" :          "",
                "moto_sold_price" :       int(temp_moto_price.replace("¥", "").replace(",", "")),
            }
            if len(temp_title_span_list) > 1 :
                temp_data["moto_year"] = temp_title_span_list[1].get_text()
            post_list.append(temp_data)
        if len(post_list) > 0:
            post_data = {"moto_list": json.dumps(post_list)}
            self.request_pool.request("POST", self.grab_notice_moto, post_data)
            page_nu = int(page_nu) + 1
            if page_nu < 6 :
                time.sleep(random.randint(2,10))
                temp_url = self.start_urls[0].format(page_no=page_nu)
                yield scrapy.Request(url=temp_url, callback=self.parse, cb_kwargs={"page_nu": str(page_nu)})
        pass
