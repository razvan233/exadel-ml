import scrapy
import csv
from bs4 import BeautifulSoup
import spacy
import re
import regex
import string
from shop_scraper.items import Product
from urllib.parse import urlparse


class ProductsSpiderSpider(scrapy.Spider):
    name = 'products_spider'
    allowed_domains = []

    def __init__(self, *args, **kwargs):
        super(ProductsSpiderSpider, self).__init__(*args, **kwargs)
        with open('../result_without_async.csv', 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if row['IsAccessible'].strip().lower() == 'true':
                    url = row['URL']
                    domain = urlparse(url).netloc
                    self.allowed_domains.append(domain)
        self.currency_pattern = re.compile(
            r'\b(?:\$|€|£|JPY|USD|EUR|GBP|INR|AUD|CAD|SGD|CNY|JPY)\b', re.IGNORECASE)
        self.currency_pattern2 = regex.compile(
            r'(?:\p{Sc}|\b(?:USD|EUR|GBP|INR|AUD|CAD|SGD|CNY|JPY)\b)\s*\d+(?:,\d{3})*(?:\.\d+)?', re.IGNORECASE)
        self.allowed_chars = set(string.ascii_letters + " .,;:-_/")
        self.non_content_keywords = [
            'header', 'footer', 'nav', 'sidebar', 'advertisement', ]
        # Load Spacy model
        self.nlp = spacy.load('../v5_product_ner_model')

    def start_requests(self):
        # Read the CSV file and start requests
        with open('../result_without_async.csv', 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if row['IsAccessible'].strip().lower() == 'true':
                    yield scrapy.Request(row['URL'].strip(), self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        for script in soup(['script', 'style', 'nav', 'header', 'footer', 'form', 'img']):
            script.extract()

        non_content_attributes = [
            ('class', 'header'),
            ('class', 'footer'),
            ('class', 'nav'),
            ('class', 'sidebar'),
            ('data-section-id', 'sidebar'),
            ('data-section-id', 'header'),
            ('data-section-id', 'footer'),
            ('data-section-id', 'nav'),
            ('id', 'sidebar'),
            ('id', 'header'),
            ('id', 'footer'),
            ('id', 'nav'),
        ]

        for attr, value in non_content_attributes:
            for element in soup.find_all(attrs={attr: value}):
                element.extract()
        for tag in soup.find_all(self.has_non_content_attribute):
            tag.extract()
        text = soup.get_text()
        text = ' '.join(text.split())

        doc = self.nlp(text)
        for ent in doc.ents:
            product = ent.text
            if self.currency_pattern.search(product) or self.currency_pattern2.search(product):
                continue
            if any(char not in self.allowed_chars for char in product):
                continue
            if '.' in product:
                product = product.split(".")[0]
            item = Product()
            item['product'] = product.lower()
            item['url'] = response.url
            yield item
            links = response.css('a::attr(href)').extract()
            for link in links:
                yield response.follow(link, self.parse)

    def has_non_content_attribute(self, tag):
        for attribute in tag.attrs.values():
            if any(keyword in str(attribute).lower() for keyword in self.non_content_keywords):
                return True
        return False
