import sys
from pprint import pprint

from icecream import ic

from constants import (
    CATEGORIES_TO_BE_DELETED,
    CATEGORY_NAME_MAX_LENGTH,
    INGREDIENTS_MAX_LENGTH,
    MINIMAL_CATEGORY_LENGTH,
    NBR_OF_FIELDS_BY_PRODUCT,
    PRODUCT_NAME_MAX_LENGTH,
    SHOP_NAME_MAX_LENGTH,
    )


class DataFormatter:
    """Formats the data that will be put into the database."""

    def __init__(self):
        pass

    def format_data(self, products):
        (prefiltered_products,
         categories,
         stores) = self.filter_data(products)

        for product in prefiltered_products:
            if len(product.get("product_name")) > PRODUCT_NAME_MAX_LENGTH:
                product["product_name"] =\
                    product["product_name"][:PRODUCT_NAME_MAX_LENGTH]

            ingredients = self.format_ingredients(product)
            product['ingredients'] = ingredients
        return prefiltered_products, categories, stores

    def filter_data(self, data):
        """
Removal of non-compliant products.
        """

        print("Filtrage en cours")

        filtered_products, categories =\
            self.filter_products_n_get_categories_from_products(data)
        stores = self.get_stores_from_products(filtered_products)

        return filtered_products, categories, stores

    def filter_products_n_get_categories_from_products(self, data):
        """
Get categories from products that have benn received from Open Food Facts"""
        prefiltered_products = []
        categories_set = set()
        for rough_product in data:
            if len(rough_product) == NBR_OF_FIELDS_BY_PRODUCT:
                categories_str = rough_product.get('categories')

                categories_to_add = categories_str.split(",")
                for category in categories_to_add:
                    category = category.strip(" ,")
                    if category and len(category) >= MINIMAL_CATEGORY_LENGTH:
                        if len(category) > CATEGORY_NAME_MAX_LENGTH:
                            category = category[:CATEGORY_NAME_MAX_LENGTH]
                        categories_set.add(category)

                prefiltered_products.append(rough_product)
        categories_list = list(categories_set)
        for category in categories_set:
            for unwanted_category in CATEGORIES_TO_BE_DELETED:
                if category == unwanted_category:
                    categories_list.remove(category)
        categories_set = set(categories_list)
        return prefiltered_products, categories_set

    def get_stores_from_products(self, data):
        """
Get stores from products that have benn received from Open Food Facts"""

        stores_set = set()
        for rough_product in data:
            stores_str = rough_product.get('stores')

            stores_to_add = stores_str.split(",")
            for store in stores_to_add:
                store = store.strip(" ,")
                store = store.title()
                if len(store) > SHOP_NAME_MAX_LENGTH:
                    store = store[:SHOP_NAME_MAX_LENGTH]
                stores_set.add(store)
        return stores_set

    def format_ingredients(self, product):
        ingredients = product.get("ingredients")
        ingredients_str = ""
        for ingredient in ingredients:
            ingredients_str += (
                str(ingredient.get("text"))
                + " "
                + str(round(float(ingredient.get('percent_estimate')), 2))
                + "% - ")

            # Sometimes an ingredient have ingredients
            if ingredient.get("ingredients"):
                inner_ingredients = ingredient.get("ingredients")
                inner_ingredients_str = ""
                for inner_ingredient in inner_ingredients:
                    inner_ingredients_str += (
                        str(inner_ingredient.get("text"))
                        + " "
                        + str(round(float(
                            inner_ingredient.get('percent_estimate')), 2))
                        + "% - ")
                ingredients_str = (ingredients_str[:-2]
                                   + "(" + inner_ingredients_str[:-3] + ") - ")
                'percent_estimate'
        if len(ingredients_str) > INGREDIENTS_MAX_LENGTH:
            ingredients_str = ingredients_str[:INGREDIENTS_MAX_LENGTH]
        return ingredients_str
