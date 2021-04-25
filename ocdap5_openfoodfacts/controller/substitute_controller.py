import sys
import time

from icecream import ic

from db.db_creator import (Product)
from constants import (
    ADDED_TO_FAV_PAGE,
    ADDED_TO_FAV_FOOD_PAGE,
    DETAILS_OF_A_BEVERAGE_PROD_PAGE,
    DETAILS_OF_A_FOOD_PROD_PAGE,
    GET_A_BETTER_BEVERAGE_PAGE,
    GET_A_BETTER_FOOD_PAGE,
    GET_PROD_FROM_A_BEVERAGE_PAGE,
    GET_PROD_FROM_A_FOOD_PAGE,
    INDEX_OF_FIRST_CAT,
    INDEX_OF_FIRST_PROD,
    LOOK_FOR_A_BETTER_PRODUCT,
    MAX_PRODS_DISPLAYED,
    NEXT_CATEGORIES,
    NEXT_PRODUCTS,
    PREVIOUS_CATEGORIES,
    PREVIOUS_PRODUCTS,
    SUBSTITUTE_A_BEVERAGE_PAGE,
    SUBSTITUTE_A_FOOD_PAGE)
from logger import logger


class SubstituteController:
    """analyse events on the substitute branch"""

    def analyze(self, controller, page_nbr, choice, args={}):
        if page_nbr == SUBSTITUTE_A_FOOD_PAGE:
            controller.manage_menu_header(choice)
            if choice in [NEXT_CATEGORIES, PREVIOUS_CATEGORIES]:
                controller.set_next_page_nbr(SUBSTITUTE_A_FOOD_PAGE)

            elif choice >= INDEX_OF_FIRST_CAT:
                controller.set_next_page_nbr(GET_PROD_FROM_A_FOOD_PAGE)
                controller.memory["subcategory_name"] = (
                    controller.get_food_subcategories()[
                        choice - INDEX_OF_FIRST_CAT])

        elif page_nbr == SUBSTITUTE_A_BEVERAGE_PAGE:
            controller.manage_menu_header(choice)
            if choice in [NEXT_CATEGORIES, PREVIOUS_CATEGORIES]:
                controller.set_next_page_nbr(SUBSTITUTE_A_BEVERAGE_PAGE)

            elif choice >= INDEX_OF_FIRST_CAT:
                controller.set_next_page_nbr(GET_PROD_FROM_A_BEVERAGE_PAGE)
                controller.memory["subcategory_name"] = (
                    controller.get_beverage_subcategories()[
                        choice - INDEX_OF_FIRST_CAT])

        elif page_nbr == GET_PROD_FROM_A_FOOD_PAGE:
            ic()
            time.sleep(3)
            controller.manage_menu_header(choice)
            if choice in [NEXT_PRODUCTS, PREVIOUS_PRODUCTS]:
                logger.info("if Précédents / suivants")
                controller.set_next_page_nbr(GET_PROD_FROM_A_FOOD_PAGE)

            elif choice >= INDEX_OF_FIRST_PROD:
                controller.set_next_page_nbr(DETAILS_OF_A_FOOD_PROD_PAGE)

                controller.memory["product"] = (
                    controller.memory["list_of_products"][
                        choice - INDEX_OF_FIRST_PROD])

        elif page_nbr == GET_PROD_FROM_A_BEVERAGE_PAGE:
            controller.manage_menu_header(choice)
            if choice in [NEXT_PRODUCTS, PREVIOUS_PRODUCTS]:
                controller.set_next_page_nbr(GET_PROD_FROM_A_BEVERAGE_PAGE)

            elif choice >= INDEX_OF_FIRST_PROD:
                controller.set_next_page_nbr(DETAILS_OF_A_BEVERAGE_PROD_PAGE)

                controller.memory["product"] = (
                    controller.memory["list_of_products"][
                        choice - INDEX_OF_FIRST_PROD])

        elif page_nbr == DETAILS_OF_A_FOOD_PROD_PAGE:
            controller.manage_menu_header(choice)
            if choice == LOOK_FOR_A_BETTER_PRODUCT:
                controller.memory["best_products"] = (
                    Product.get_better_prods(
                        controller.memory["product"],
                        controller.memory["subcategory_name"]))
                controller.set_next_page_nbr(GET_A_BETTER_FOOD_PAGE)

        elif page_nbr == DETAILS_OF_A_BEVERAGE_PROD_PAGE:
            controller.manage_menu_header(choice)
            if choice == LOOK_FOR_A_BETTER_PRODUCT:
                controller.memory["best_products"] = (
                    Product.get_better_prods(
                        controller.memory["product"],
                        controller.memory["subcategory_name"]))
                controller.set_next_page_nbr(GET_A_BETTER_BEVERAGE_PAGE)

        elif page_nbr == GET_A_BETTER_FOOD_PAGE:
            controller.manage_menu_header(choice)
            if (choice >= INDEX_OF_FIRST_PROD
                    and (choice - INDEX_OF_FIRST_PROD) < MAX_PRODS_DISPLAYED):

                controller.memory["fav_prod"] = (
                    controller.memory["best_products"][
                        choice - INDEX_OF_FIRST_PROD][0])

                Product.add_favorite(
                    controller.memory["product"],
                    controller.memory["fav_prod"])

                controller.set_next_page_nbr(ADDED_TO_FAV_FOOD_PAGE)

        elif page_nbr == GET_A_BETTER_BEVERAGE_PAGE:
            controller.manage_menu_header(choice)
            if (choice >= INDEX_OF_FIRST_PROD
                    and (choice - INDEX_OF_FIRST_PROD) < MAX_PRODS_DISPLAYED):

                controller.memory["fav_prod"] = (
                    controller.memory["best_products"][
                        choice - INDEX_OF_FIRST_PROD][0])

                Product.add_favorite(
                    controller.memory["product"],
                    controller.memory["fav_prod"])

                controller.set_next_page_nbr(ADDED_TO_FAV_PAGE)
        else:
            controller.home_page()
