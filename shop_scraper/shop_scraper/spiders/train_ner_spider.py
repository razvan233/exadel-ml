import scrapy
from bs4 import BeautifulSoup


class EcomSpider(scrapy.Spider):
    name = "ecom_spider"
    allowed_domains = ["factorybuys.com.au"]
    start_urls = [
        'https://www.factorybuys.com.au/collections/instabadge-best-selling/products/queen-size-gas-lift-bed-frame-charcoal']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        for script in soup(['script', 'style', 'nav', 'header', 'footer']):
            script.extract()

        cleaned_content = str(soup)

        description = self.extract_description(
            cleaned_content)
        if description:

            self.save_annotation(description)
        links = response.css('a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse)

    def extract_description(self, content):
        soup = BeautifulSoup(content, 'lxml')
        description_tag = soup.find('div', class_='description-custom-content')
        if description_tag:
            description = description_tag.get_text(strip=True)
            if description:
                return description
        return None

    def save_annotation(self, description):
        with open('product_description_without_labels.txt', 'a') as f:
            f.write(
                f"{description}\n")
