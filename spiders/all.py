from .bike24_spider import Bike24Spider
from .bike_components_spider import BikeComponentsSpider
from .bike_discount_spider import BikeDiscountSpider


spiders = {
    'bike24' : Bike24Spider,
    'bike_components' : BikeComponentsSpider,
    'hibike': BikeDiscountSpider,
}


def get_result_as_text(stores, category, item_name):
    resulted_list = []
    spiders_of_stores = [spiders[store_name] for store_name in spiders if store_name in stores]

    for spider in spiders_of_stores:
        res = spider(category, item_name).run()
        resulted_list.extend(res)

    text = repr_in_text(resulted_list)
    return text


def repr_in_text(resulted_list):
    text = ''
    print(resulted_list, sep='\n')
    for inc, item in enumerate(resulted_list, 1):
        name = list(item.keys())[0]
        price = list(item.values())[0][0]
        url = list(item.values())[0][1]
        text += f'{inc}. <b>{price}€</b> {name} \n<a href="{url}">{url[:35]}...</a>\n'

    return text