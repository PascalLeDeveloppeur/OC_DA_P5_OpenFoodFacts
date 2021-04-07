import sys

from icecream import ic

from constants import (
    CREATE_DB_PAGE,
    DB_HAS_BEEN_CREATED,
    DETAILS_OF_A_BEVERAGE_PROD_PAGE,
    GET_PROD_FROM_A_SUBCAT_PAGE,
    HOME_PAGE,
    INITIAL_PAGE,
    SUBSTITUTE_A_BEVERAGE_PAGE,
    SUBSTITUTE_A_FOOD)


class Router:
    """Take user to wanted page"""

    def __init__(self):
        pass

    def go_to(self, controller, elt={}):
        next_page = controller.get_next_page()

        # Branch: starter
        if next_page == INITIAL_PAGE:
            controller.run()
        elif next_page == CREATE_DB_PAGE:
            controller.create_db_page()
        elif next_page == HOME_PAGE:
            controller.home_page()

        # Branch: Substitute a beverage
        elif next_page == SUBSTITUTE_A_BEVERAGE_PAGE:
            controller.substitute_a_beverage()
        elif next_page == GET_PROD_FROM_A_SUBCAT_PAGE:
            controller.get_prod_from_a_subcat(
                elt.get("subcategory_of_beverage"))
        elif next_page == DETAILS_OF_A_BEVERAGE_PROD_PAGE:
            controller.details_of_a_beverage_prod(
                elt.get("subcategory_of_beverage"))

        # Branch: Substitute a food
        elif next_page == SUBSTITUTE_A_FOOD:
            controller.substitute_a_food()

        # Branch: Watch my fav
        elif next_page == 301:
            controller.favorites_page()
        elif next_page == 302:
            controller.fav_product_page()

        # Branch: root db creator
        elif next_page == DB_HAS_BEEN_CREATED:
            controller.db_created_page()

        # Home page
        else:
            controller.home_page()
