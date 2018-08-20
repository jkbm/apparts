import scrapy

class AppartmentsSpider(scrapy.Spider):
    name = "appartments"

    start_urls = ["https://www.olx.ua/nedvizhimost/kvartiry-komnaty/arenda-kvartir-komnat/kvartira/kiev/?search%5Bfilter_float_price%3Afrom%5D=7000&search%5Bfilter_float_price%3Ato%5D=8000&search%5Bfilter_float_number_of_rooms%3Afrom%5D=2&search%5Bfilter_float_number_of_rooms%3Ato%5D=2&search%5Bphotos%5D=1"]
            
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'appartments-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        SET_SELECTOR = ".offer"
        PRICE_SELECTOR = './/p[@class="price"]/strong/text()'
        DISTRICT_TIME_SELECTOR = '*//td[@class="bottom-cell"]//span/text()'
        TITLE_SELECTOR = './/*[@class="title-cell"]//strong/text()'
        LINK_SELECTOR = './/*[@class="title-cell"]//a/@href'
        for offer in response.css(SET_SELECTOR):
            if "Сегодня" in offer.xpath(DISTRICT_TIME_SELECTOR).extract()[3].strip():
                yield {
                    "title": offer.xpath(TITLE_SELECTOR).extract_first(),
                    "link": offer.xpath(LINK_SELECTOR).extract_first(),
                    "price": offer.xpath(PRICE_SELECTOR).extract_first(),
                    "district": offer.xpath(DISTRICT_TIME_SELECTOR).extract()[1].strip(),
                    "time": offer.xpath(DISTRICT_TIME_SELECTOR).extract()[3].strip(),

                }