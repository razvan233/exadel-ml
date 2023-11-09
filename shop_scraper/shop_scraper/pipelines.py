# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv
from scrapy.exceptions import DropItem


class ShopScraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveItem:
    def open_spider(self, spider):
        self.file = open('products_list_by_url_from_model_v5.csv',
                         'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.seen = set()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        identifier = tuple(item.items())
        if identifier in self.seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.seen.add(identifier)
            self.writer.writerow([item['url'], item['product']])
            return item
