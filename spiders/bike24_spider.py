from category_codes.bike24_category_codes import bike24_category_codes
from bs4 import BeautifulSoup
from .baseSpider import AbstractSpider


class Bike24Spider(AbstractSpider):
    CATEGORY_CODES = bike24_category_codes
    TEMPLATE_URL = r'https://www.bike24.com/search/catalog-{}?searchTerm={}'

    def __init__(self, category, item_name):
        super().__init__(category, item_name)

    def get_list_items(self):
        req = self.get_html()
        soup = BeautifulSoup(req, 'lxml')
        ul = soup.find(class_='col-md-18 print')
        list_items = ul.find_all(
            class_='box-product-list-item box-product-list-item-outlet js-product-link js-product-link-parent')
        return list_items

    def scrape_data(self, item):
        name = item.find(class_='text-title h4').a['title']
        price_string = item.find(class_='text-price').text
        price = self.price_to_float(price_string)
        url = item.find(class_='text-title h4').a['href']
        cell = {name: [price, url]}
        return cell

    def price_to_float(self, price_string):
        return float(price_string.split('€')[-1][:-1].replace(',', '.'))

