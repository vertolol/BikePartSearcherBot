from abc import ABC, abstractmethod
import requests


class AbstractSpider(ABC):
    CATEGORY_CODES = None
    TEMPLATE_URL = None
    SIZE = 3

    def __init__(self, category, item_name):
        self.category_code = self.CATEGORY_CODES[category]['code']
        self.item_name = item_name
        if self.CATEGORY_CODES[category]['additional_string'] is not None:
            self.item_name = item_name + ' ' + self.CATEGORY_CODES[category]['additional_string']

    def get_html(self):
        return requests.get(self.url).text

    def get_json(self):
        return requests.get(self.url).json()

    @property
    def url(self):
        return self.TEMPLATE_URL.format(self.category_code, self.item_name.replace(' ', '%20'))

    @abstractmethod
    def get_list_items(self):
        pass

    @abstractmethod
    def scrape_data(self, item):
        pass

    @abstractmethod
    def price_to_float(self, price_string):
        pass

    def item_name_verification(self, cell):
        words_in_item_name = self.item_name.lower().split()
        words_in_result_name = list(cell.keys())[0].lower().split()
        if all(word in words_in_result_name for word in words_in_item_name):
            return cell
        return None

    def run(self):
        result_list = []
        for item in self.get_list_items():
            cell = self.scrape_data(item)
            if self.item_name_verification(cell) is not None:
                result_list.append(cell)

        result_list.sort(key=lambda x: list(x.values())[0][0])
        return result_list[:self.SIZE]


# s = BikeComponentsSpider('mtb_27_wheels', 'DT SWISS E 1900 SPLINE')
# print(*s.run(), sep='\n')
