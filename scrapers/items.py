# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Item, Field
from itemloaders.processors import Join, MapCompose, TakeFirst
import re

def get_price(text):
    price = re.search(r'^(.*?)([\d\.,]+)', text)
    if not price:
        raise ValueError("Can't extract price")
    price = float(price.group(2).replace('.', ''))
    return price

class ProductItem(Item):
    name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    _id = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image= Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(get_price),
        output_processor=TakeFirst()
    )
    product_url = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    product_id = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    category = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    retail = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    trailer_url = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
