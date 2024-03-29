import sys
from pprint import pprint
import time

from sqlalchemy.sql import elements

from icecream import ic

from constants import (
    BAD_CATEGORIES,
    BRAND_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    INGREDIENTS_MAX_LENGTH,
    NON_FRENCH_LETTERS,
    PRODUCT_NAME_MAX_LENGTH,
    STORE_NAME_MAX_LENGTH)


class DataFormatter:
    """Formats the data that will be put into the database of the
    application."""

    def prefilter_products(self, products):
        """
En: Removes products that do not have all the required fields.
Fr: Supprime les produits qui n'ont pas tous les champs requis."""

        in_conformity_products = []
        for product in products:
            product = self.check_if_required_fields_in_product(product)
            product = self.delete_foreign_product(product)
            product = self.delete_prod_with_unknown_pnns_group_1(product)
            if product:
                in_conformity_products.append(product)
        return in_conformity_products

    def check_if_required_fields_in_product(self, product):
        """Return the product entered in argument if it has all the required
        fields otherwise return nothing.

        Args:
            product (object): Product to get verified

        Returns:
            object or nothing: The product entered in argument if it has all
            the required fields otherwise return nothing.
        """
        if (
                product.get('brands')
                and product.get('categories')
                and product.get("generic_name_fr")
                and product.get("nutriscore_grade")
                and product.get("pnns_groups_1")
                and product.get("product_name")
                and product.get("url")):
            return product
        return

    def delete_foreign_product(self, product):
        """Return the product entered in argument if it does not contain a non-french
        letter in its ingredients or a foreign category otherwise return
        nothing.

        Args:
            product (object): Product to get verified

        Returns:
            object or nothing: The product entered in argument if it is not
            detected as a foreign product otherwise return nothing.
        """
        if product:
            for foreign_letter in NON_FRENCH_LETTERS:
                if foreign_letter in str(product.get("ingredients", "")):
                    return
            return product

    def delete_prod_with_unknown_pnns_group_1(self, product):
        """Return the product entered in argument if the "pnns_groups_1" key
        is not unknown otherwise return None.

        Args:
            product (object): Product to get verified

        Returns:
            object or None: The product entered in argument if the
            "pnns_groups_1" key is not unknown otherwise return None.
        """
        if product:
            if len(product.get("pnns_groups_1")) > 2:
                return (
                    None if product.get("pnns_groups_1").lower() == "unknown"
                    else product)

    def format_products(self, controller, products):
        """
En: Formats products to optimize their utilization.
Fr: Formate les produits de façon à optimiser leur exploitation."""

        brands = set()
        categories = set()
        stores = set()
        for product in products:
            product = self.format_lists_in_product(controller, product)
            if product:

                product["product_name"] = self.format_element(
                    controller,
                    product["product_name"])[:PRODUCT_NAME_MAX_LENGTH]

                product["pnns_groups_1"] = self.format_element(
                    controller,
                    product["pnns_groups_1"])[:PRODUCT_NAME_MAX_LENGTH]

                product["description"] = (
                    product["generic_name_fr"][:DESCRIPTION_MAX_LENGTH])

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
        categories = set(self.verify_categories(categories))

        return brands, categories, products, stores

    def format_lists_in_product(self, controller, product):
        """
En: Reformats the different lists of each product.
Fr: Reformate les différentes listes de chaque produit."""

        if (product.get("categories")
                and product.get("stores")
                and product.get("brands")):

            product["categories"] = self.str_to_list(
                controller,
                product["categories"],
                CATEGORY_NAME_MAX_LENGTH)

            product["stores"] = self.str_to_list(
                controller,
                product["stores"],
                STORE_NAME_MAX_LENGTH)

            product["brands"] = self.str_to_list(
                controller,
                product["brands"],
                BRAND_NAME_MAX_LENGTH)

            return product
        return

    def str_to_list(self,
                    controller,
                    data_str,
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
            element = self.format_element(controller, element)

            filtered_data_list.append(element)

            if "Aliments" in element:
                filtered_data_list.append("Aliments")

        return filtered_data_list

    def format_element(self, controller, element):
        """
En: Format the name of the element.
Fr: Formate le nom de l'élément."""

        element = element.title()
        element = controller.remove_accent(element)
        return element

    def format_ingredients(self, product):
        """Extracts the list of ingredients from a product and convert it to a string.
        Args:
            product (object): Downloaded product

        Returns:
            string: List of ingredients
        """
        ingredients_str = ""
        ingredients = product.get("ingredients")
        if ingredients:
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

    def remove_unwanted_category(self, category):
        """Return nothing if the category is in a list of unwanted categories.
        Else return the category

        Args:
            category (string): Category to check

        Returns:
            string or nothing: The entered category if it is not in a list of
            unwanted categories.
        """
        for bad_category in BAD_CATEGORIES:
            if category.startswith(bad_category):
                return
        return category

    def verify_categories(self, categories):
        """Remove unwanted categories from the list of categories

        Args:
            categories (list of strings): List of unfiltered categories

        Returns:
            list of strings: Filtered categories
        """
        return [self.remove_unwanted_category(category)
                for category in categories]
