import requests
import sys

from pprint import pprint

from constants import (
    WANTED_FIELDS_OF_A_PRODUCT,
    NBR_OF_PAGES,
    PRODUCTS_PER_PAGE)


class DataDownloader:
    """Download data from OpenFoodFacts to populate the local database."""

    def rough_products(self):
        return self.__rough_products

    def set_rough_products(self, rough_products):
        self.__rough_products = rough_products

    def download(self):
        rough_products = []
        url = "https://fr.openfoodfacts.org/cgi/search.pl"
        for page_nbr in range(NBR_OF_PAGES):
            params = {
                "action": "process",
                "sort_by": "unique_scan_n",
                "search_terms": "aliments",
                "fields": WANTED_FIELDS_OF_A_PRODUCT,
                "page_size": f"{PRODUCTS_PER_PAGE}",
                "json": "1",
                "page": f"{page_nbr + 1}"}

            response = requests.get(url, params=params)
            rough_data = response.json()
            rough_products += rough_data.get('products')

        for page_nbr in range(NBR_OF_PAGES):
            params = {
                "action": "process",
                "sort_by": "unique_scan_n",
                "search_terms": "boissons",
                "fields": WANTED_FIELDS_OF_A_PRODUCT,
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": "boissons",
                "page_size": f"{PRODUCTS_PER_PAGE}",
                "json": "1",
                "page": f"{page_nbr + 1}"}

            response = requests.get(url, params=params)
            rough_data = response.json()
            rough_products += rough_data.get('products')

        return rough_products
