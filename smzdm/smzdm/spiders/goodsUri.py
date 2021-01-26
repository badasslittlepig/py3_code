import scrapy


class GoodsuriSpider(scrapy.Spider):
    name = 'goodsUri'
    allowed_domains = ['search.smzdm.com']
    start_urls = ['https://search.smzdm.com/?c=home&s=%E5%8F%AF%E4%B9%90&order=time']

    def parse(self, response):
        html = response.text
        soup = BeautifulSoup(html, "html5lib")

        print(html)


var widget = className("android.widget.ImageView").depth(4).findOne();
click(widget.bounds().centerX(), widget.bounds().centerY());