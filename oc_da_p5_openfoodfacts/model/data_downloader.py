import requests

from constants import PRODUCTS_PER_PAGE


class DataDownloader:
    """Download data from OpenFoodFacts to populate the local database."""

    def __init__(self):
        pass

    def rough_products(self):
        return self.__rough_products

    def set_rough_products(self, rough_products):
        self.__rough_products = rough_products

    def download(self):
        rough_products = []
        for page_nbr in range(10):
            url = ("https://fr.openfoodfacts.org/cgi/search.pl"
                   + "?action=process"
                   + "&sort_by=unique_scan_n"
                   + "&fields=product_name,nutriscore_grade,"
                   + "categories,stores,brands,ingredients"
                   + f"&page_size={PRODUCTS_PER_PAGE}"
                   + f"&json=1&page={page_nbr + 1}")
            response = requests.get(url)
            rough_data = response.json()
            rough_products += rough_data.get('products')
        return rough_products
