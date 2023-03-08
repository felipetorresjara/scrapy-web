import scrapy
from scrapers.items import ProductItem
from scrapy.loader import ItemLoader
import re

url_cat = {
    "https://www.eneba.com/latam/store/action-games": "100",
    "https://www.eneba.com/latam/store/adventure-games": "200",
    "https://www.eneba.com/latam/store/fighting-games": "1100",
    "https://www.eneba.com/latam/store/fps-games": "600",
    "https://www.eneba.com/latam/store/indie-games": "300",
    "https://www.eneba.com/latam/store/mmo-games": "400",
    "https://www.eneba.com/latam/store/platform-games": "1200",
    "https://www.eneba.com/latam/store/racing-games": "1000",
    "https://www.eneba.com/latam/store/rpg-games": "400",
    "https://www.eneba.com/latam/store/simulation-games": "700",
    "https://www.eneba.com/latam/store/sport-games": "900",
    "https://www.eneba.com/latam/store/strategy-games": "500"
}

urls = ['https://www.eneba.com/latam/store/action-games', 'https://www.eneba.com/latam/store/adventure-games', 'https://www.eneba.com/latam/store/fighting-games', 'https://www.eneba.com/latam/store/fps-games', 'https://www.eneba.com/latam/store/indie-games', 'https://www.eneba.com/latam/store/mmo-games', 'https://www.eneba.com/latam/store/platform-games', 'https://www.eneba.com/latam/store/racing-games', 'https://www.eneba.com/latam/store/rpg-games', 'https://www.eneba.com/latam/store/simulation-games', 'https://www.eneba.com/latam/store/sport-games', 'https://www.eneba.com/latam/store/strategy-games']

#urls = ['https://www.eneba.com/latam/store/racing-games']

class EnebaSpider(scrapy.Spider):
    name = "eneba"
    start_urls = urls
    cookies = {
        'exchange':'CLP',
        'region': 'chile',
        'lng': 'latam'
    }
    eneba_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'cookie': 'userId=160464471457753534233800455110724; zd=10; __utmzzses=1; region=chile; crt=b4f33ad18e93423ca08db6dac89ac4fa; lng=latam; isLang=1; cconsent=1; _fbp=fb.1.1652655558130.683464707; scm=d.chile.bafc981e32e91f25.3445cbecef9f72139d6d7728039ff9845564105120499e6d98d989102f6fd590; PHPSESSID_=0825o9pgjnvh9d55shgtevecb2; exchange=CLP',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'es-419,es;q=0.9',
        'expect-ct': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct',
        'cache-control': 'max-age=0',
    }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.eneba_headers, cookies=self.cookies)

    def parse(self, response):
        print(response.request.url)
        products = response.css('div.pFaGHa.WpvaUk')
        for prod in products:
            stock = prod.css('div.EoJMSg span.kq4D4Y::text').get()
            if stock == 'Agotado':
                continue
            loader = ItemLoader(item=ProductItem(), selector=prod)
            product_url = 'https://www.eneba.com' + prod.css('a.oSVLlh::attr(href)').get()
            image = prod.css('div.AYvEf0 img::attr(src)').get()
            print("imagen:")
            print(image)
            _id = re.search( r'(?<=resized-products\/)([A-Z-a-z-0-9-_]+)(?=_350)', image).group(1)
            print("id: ", _id)
            loader.add_css('name', 'span.YLosEL::text')
            loader.add_value('_id', _id)
            loader.add_value('product_id', _id)
            loader.add_value('image', image)
            loader.add_value('product_url', product_url)
            loader.add_value('category', url_cat[response.request.url.split('?')[0]])
            loader.add_css('price', 'span.DTv7Ag span.L5ErLT::text')
            loader.add_value('retail', 'eneba')
            yield loader.load_item()
        disabled_next_page = response.css('li.rc-pagination-next::attr(aria-disabled)').get()
        if disabled_next_page == 'false':
            next_page = response.css('li.rc-pagination-next a::attr(href)').get()
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)

