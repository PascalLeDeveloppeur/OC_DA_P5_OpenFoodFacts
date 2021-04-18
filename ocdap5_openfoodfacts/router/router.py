import sys
import time

from icecream import ic

from logger import logger
from constants import (
    ADDED_TO_FAV_PAGE,
    ADDED_TO_FAV_FOOD_PAGE,
    CREATE_DB_PAGE,
    DB_HAS_BEEN_CREATED,
    DETAILS_OF_A_BEVERAGE_PROD_PAGE,
    DETAILS_OF_A_FOOD_PROD_PAGE,
    GET_A_BETTER_BEVERAGE_PAGE,
    GET_A_BETTER_FOOD_PAGE,
    GET_PROD_FROM_A_BEVERAGE_PAGE,
    GET_PROD_FROM_A_FOOD_PAGE,
    HOME_PAGE,
    INITIAL_PAGE,
    SUBSTITUTE_A_BEVERAGE_PAGE,
    SUBSTITUTE_A_FOOD_PAGE)


class Router:
    """Take user to wanted page"""

    def __init__(self):
        pass

    def go_to(self, controller):
        ic()
        time.sleep(3)
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
        elif next_page == GET_PROD_FROM_A_BEVERAGE_PAGE:
            controller.get_prod_from_a_beverage()
        elif next_page == DETAILS_OF_A_BEVERAGE_PROD_PAGE:
            controller.details_of_a_beverage_prod()
        elif next_page == GET_A_BETTER_BEVERAGE_PAGE:
            controller.get_a_better_beverage()
        elif next_page == ADDED_TO_FAV_PAGE:
            controller.added_to_fav()

        # Branch: Substitute a food
        elif next_page == SUBSTITUTE_A_FOOD_PAGE:
            ic()
            time.sleep(3)
            controller.substitute_a_food()
        elif next_page == GET_PROD_FROM_A_FOOD_PAGE:
            controller.get_prod_from_a_food()
        elif next_page == DETAILS_OF_A_FOOD_PROD_PAGE:
            controller.details_of_a_food_prod()
        elif next_page == GET_A_BETTER_FOOD_PAGE:
            controller.get_a_better_food()
        elif next_page == ADDED_TO_FAV_FOOD_PAGE:
            controller.added_to_fav_food()

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
