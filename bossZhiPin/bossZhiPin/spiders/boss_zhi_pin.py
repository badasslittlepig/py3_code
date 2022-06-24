import random
import time
import scrapy
import json
import urllib3

class BossZhiPinSpider(scrapy.Spider):
    name = 'boss_zhi_pin'
    allowed_domains = ['www.zhipin.com']
    start_urls      = ['https://www.zhipin.com/wapi/zpgeek/miniapp/search/joblist.json?query=%E5%8F%B8%E6%9C%BA&city=101020100&source=undefined&stage=&scale=&degree=&industry=&salary=&experience=&sortType=0&subwayLineId=&subwayStationId=&districtCode=&businessCode=&longitude=&latitude=&position=&expectId=&expectPosition=&page={page_no}&pageSize=10&appId=10002']
    job_grab_uri    = "http://test.skyshappiness.com/index.php?m=Open&c=BossGrab&a=jobAdd"
    request_pool    = urllib3.PoolManager()

    def start_requests(self):
        page_nu = "1"
        temp_url = self.start_urls[0].format(page_no=page_nu)
        yield scrapy.Request(url=temp_url, callback=self.parse, cb_kwargs={"page_nu":page_nu})

    def parse(self, response, page_nu):
        body_str = response.body.decode("utf-8")
        return_data = json.loads(body_str)
        if return_data['code'] == 0 :
            post_api_data = []
            job_list = return_data['zpData']['list']
            for job_info in job_list:
                temp_info = {}
                temp_info["job_name"]       = job_info["jobName"]
                temp_info["job_experience"] = job_info["jobExperience"]
                temp_info["job_degree"]     = job_info["jobDegree"]
                temp_info["district_name"]  = job_info["districtName"]
                temp_info["business_name"]  = job_info["businessName"]
                temp_info["performance"]    = job_info["performance"]
                temp_info["salary_desc"]    = job_info["salaryDesc"]
                temp_info["job_labels"]     = ",".join(job_info["jobLabels"])
                temp_info["skills"]         = ",".join(job_info["skills"])
                temp_info["encrypt_jobid"]  = job_info["encryptJobId"]
                post_api_data.append(temp_info)
            post_data = {"job_list": json.dumps(post_api_data)}
            self.request_pool.request("POST", self.job_grab_uri, post_data)
        
        if return_data['zpData']['hasMore']:
            time.sleep(random.randint(2,10))
            page_nu = str(int(page_nu) + 1)
            temp_url = self.start_urls[0].format(page_no=page_nu)
            yield scrapy.Request(url=temp_url, callback=self.parse, cb_kwargs={"page_nu":page_nu})
        pass
