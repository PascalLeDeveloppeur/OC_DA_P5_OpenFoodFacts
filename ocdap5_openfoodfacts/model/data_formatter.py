import sys
from pprint import pprint

from sqlalchemy.sql import elements

from icecream import ic

from constants import (
    BRANDS,
    BRAND_NAME_MAX_LENGTH,
    CATEGORIES,
    CATEGORIES_TO_BE_DELETED,
    CATEGORY_NAME_MAX_LENGTH,
    INGREDIENTS_MAX_LENGTH,
    MINIMAL_CATEGORY_LENGTH,
    NBR_OF_FIELDS_BY_PRODUCT,
    PRODUCT,
    PRODUCT_NAME_MAX_LENGTH,
    STORES,
    STORE_NAME_MAX_LENGTH)


class DataFormatter:
    """Formats the data that will be put into the database."""

    def __init__(self):
        pass

    def filter_data(self, rough_products):
        """
Removal of non-compliant products.
        """

        print("Filtrage en cours")

        filtered_products, categories =\
            self.filter_products_n_get_categories_from_products(rough_products)
        stores = self.get_stores_from_products(filtered_products)

        return filtered_products, categories, stores

    def filter_products_n_get_categories_from_products(self, rough_products):
        """
Get categories from products that have been received from Open Food Facts"""
        prefiltered_products = []
        categories_set = set()
        for rough_product in rough_products:
            if len(rough_product) == NBR_OF_FIELDS_BY_PRODUCT:
                categories_str = rough_product.get('categories')

                categories_to_add = categories_str.split(",")
                rough_product['categories'] = categories_to_add
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

    def prefilter_products(self, products):
        """
En: Removes products that do not have all the required fields.
Fr: Supprime les produits qui n'ont pas tous les champs requis."""

        in_conformity_products = []
        for product in products:
            product = self.check_if_required_fields_in_product(product)
            if product:
                in_conformity_products.append(product)
        return in_conformity_products

    def check_if_required_fields_in_product(self, product):
        if not product.get("categories"):
            return []
        if not product.get("brands"):
            return []
        if not product.get("product_name"):
            return []
        return product

    def format_products(self, controller, products):
        """
En: Formats products to optimize their utilization.
Fr: Formate les produits de façon à optimiser leur exploitation."""

        brands = set()
        categories = set()
        stores = set()
        for product in products:
            product = self.format_lists_in_product(controller, product)

            product["product_name"] = self.format_element(
                                    controller,
                                    product["product_name"],
                                    PRODUCT)[:PRODUCT_NAME_MAX_LENGTH]

            product["ingredients"] = self.format_ingredients(
                                    product)[:INGREDIENTS_MAX_LENGTH]

            self.add_to_set(controller,
                            product["categories"],
                            categories,
                            CATEGORY_NAME_MAX_LENGTH)

            self.add_to_set(controller,
                            product["brands"],
                            brands,
                            BRAND_NAME_MAX_LENGTH)

            self.add_to_set(controller,
                            product["stores"],
                            stores,
                            STORE_NAME_MAX_LENGTH)

        return brands, categories, products, stores

    def format_lists_in_product(self, controller, product):
        """
En: Reformats the different lists of each product.
Fr: Reformate les différentes listes de chaque produit."""

        product["categories"] = self.str_to_list(
            controller,
            product["categories"],
            CATEGORIES,
            CATEGORY_NAME_MAX_LENGTH)

        product["stores"] = self.str_to_list(
            controller,
            product["stores"],
            STORES,
            STORE_NAME_MAX_LENGTH)

        product["brands"] = self.str_to_list(
            controller,
            product["brands"],
            BRANDS,
            BRAND_NAME_MAX_LENGTH)

        return product

    def str_to_list(self,
                    controller,
                    data_str,
                    data_name,
                    max_length_of_element_in_data):
        """
En: Transforms a list that is in string form into a standard list structure.
    Each element of the list does not exceed the maximum size allowed in the
    argument.
Fr: Transforme une liste qui est sous forme de chaîne de caractères en liste
standard.
    Chaque élément de la liste ne dépasse pas la taille maximale autorisée
    en argument."""

        filtered_data_list = []
        data_list = data_str.split(",")
        for element in data_list:
            element = element.strip(" ,")[:max_length_of_element_in_data]
            element = self.format_element(controller, element, data_name)

            filtered_data_list.append(element)

            # En:   Adding the "Aliments" (food) category.
            # Fr:   Ajout de la catégorie «Aliments».
            if "Aliments" in element:
                filtered_data_list.append("Aliments")

        return filtered_data_list

    def format_element(self, controller, element, data_name):
        """
En: Format the name of the element.
Fr: Formate le nom de l'élément."""

        element = element.title()
        element = controller.remove_accent(element)
        return element

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
                inner_ingredients_str = "".join((
                        str(inner_ingredient.get("text"))
                        + " "
                        + str(round(float(
                            inner_ingredient.get('percent_estimate')), 2))
                        + "% - ") for inner_ingredient in inner_ingredients)
                ingredients_str = (ingredients_str[:-2]
                                   + "(" + inner_ingredients_str[:-3] + ") - ")
                'percent_estimate'
        if len(ingredients_str) > INGREDIENTS_MAX_LENGTH:
            ingredients_str = ingredients_str[:INGREDIENTS_MAX_LENGTH]
        return ingredients_str

    def add_to_set(self,
                   controller,
                   data_origin,
                   data_set_destination,
                   data_max_length):
        """
En: Format and add each element to the set.
Fr: Formate puis ajoute chaque élément au set."""
        for data in data_origin:
            data = controller.remove_accent(data)
            data_set_destination.add(data[:data_max_length])
