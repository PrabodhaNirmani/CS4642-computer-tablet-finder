import scrapy


class ComputersSpider(scrapy.Spider):
    name = "computers"
    start_urls = [
        'https://ikman.lk/en/ads/colombo/computers-tablets?categoryType=ads&categoryName=Computers+%26+Tablets&type'
        '=for_sale',
    ]

    def parse(self, response):
        # follow links to computers pages
        for href in response.css('div.item-content a::attr(href)'):
            yield response.follow(href, self.parse_computers)

        # follow pagination links
        for href in response.css('div.col-6 a.pag-number::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_computers(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        # define properties()
        attribute_type = response.css('div.item-properties dt::text').extract()
        attribute_value = response.css('div.item-properties dd::text').extract()

        properties = {}
        for i in range(0, len(attribute_type)):
            properties[attribute_type[i]] = attribute_value[i]

        def extract_attribute(property):
            value = ''
            if property in properties.keys():
                value = properties[property]
            return value

        yield{
            'item_name': extract_with_css('div.item-top h1::text'),
            'sale_by': extract_with_css('span.poster a::text'),
            'date': extract_with_css('span.date::text'),
            'location': extract_with_css('span.location::text'),
            'price': extract_with_css('span.amount::text'),
            'condition': extract_attribute('Condition:'),
            'item_type': extract_attribute('Device type:'),
            'brand': extract_attribute('Brand:'),
            'model': extract_attribute('Model:'),
            'description': response.css('div.item-description p::text').extract(),

        }
