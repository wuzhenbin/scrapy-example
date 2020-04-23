from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Join, Compose, MapCompose


class BaseLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
class quoteLoader(BaseLoader):
    tags_out = MapCompose(str.upper)
