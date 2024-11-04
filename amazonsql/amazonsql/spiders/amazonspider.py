import scrapy
from amazonsql.items import AmazonsqlItem


class AmznspiderSpider(scrapy.Spider):
    name = "amznspider"
    start_urls = ["https://www.amazon.com/s?k=raspberry+pi+5+single+board&crid=1FHMWHXAFR5CN&qid=1730206804&sprefix=raspberry+pi+5+singl%2Caps%2C434&ref=sr_pg_1"]

    max_pages = 18
    page_count = 0

    def parse(self, response):
        
        for rpi in response.xpath('//div[@class="a-section"]'):
            product = AmazonsqlItem()

            product["name"] = rpi.xpath('.//h2//a//span/text()').get()
            if product["name"] is None:
                continue

            product["price"] = rpi.xpath('.//span[@class="a-price"]//span[@class="a-offscreen"]/text()').get()


            product["ratings"] = rpi.xpath('.//span[@class="rush-component"]//span/@aria-label').get()
            if product["ratings"]:
                product["ratings"] = product["ratings"].replace('ratings', '').strip()
            else:
                product["ratings"] = "No ratings yet"


            product["stars"] = rpi.xpath('.//a//span[@class="a-icon-alt"]/text()').get()
            if product["stars"]:
                product["stars"] = product["stars"].split()[0]
            else:
                product["stars"] = "No stars yet"

            yield product

        if self.page_count < self.max_pages:
            self.page_count += 1
            next_page = f"https://www.amazon.com/s?k=raspberry+pi+5&page={self.page_count}&crid=3WA0DKU7FS6L&qid=1730294680&sprefix=raspberry+pi+5+s%2Caps%2C556&ref=sr_pg_{self.page_count}"
            yield response.follow(next_page, self.parse)

        
