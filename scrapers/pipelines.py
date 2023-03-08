# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient

class ScrapersPipeline:
    def __init__(self):
        #example mongo link
        self.client = MongoClient('mongodb+srv://user_node_example:PvO6Bc4lGmXWsdZj@micluster.shtovoy.mongodb.net/storeDB')
    def process_item(self, item, spider):
        #db = self.client.cl
        db = self.client.storeDB
        collection = db.products
        collection.insert_one(item)
        return item
