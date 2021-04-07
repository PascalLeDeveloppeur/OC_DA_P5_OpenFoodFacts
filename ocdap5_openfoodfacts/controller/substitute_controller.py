import sys
import time

from icecream import ic

from constants import (
    DETAILS_OF_A_BEVERAGE_PROD_PAGE,
    GET_PROD_FROM_A_SUBCAT_PAGE,
    INDEX_OF_FIRST_CAT,
    INDEX_OF_FIRST_PROD,
    NEXT_CATEGORIES,
    NEXT_PRODUCTS,
    PREVIOUS_CATEGORIES,
    PREVIOUS_PRODUCTS,
    SUBSTITUTE_A_BEVERAGE_PAGE)
from logger import logger


class SubstituteController:
    """analyse events on the substitute branch"""

    def __init__(self):
        pass

    def analyze(self, controller, page_nbr, choice, args={}):
        logger.info(ic())
        if page_nbr == SUBSTITUTE_A_BEVERAGE_PAGE:
            print("SUBSTITUTE_A_BEVERAGE_PAGE")
            controller.manage_menu_header(choice)
            if choice in [NEXT_CATEGORIES, PREVIOUS_CATEGORIES]:
                print("NEXT_CATEGORIES, PREVIOUS_CATEGORIES")
                print(ic())
                time.sleep(3)
                # import ipdb; ipdb.set_trace()
                controller.set_next_page_nbr(SUBSTITUTE_A_BEVERAGE_PAGE)

            elif choice >= INDEX_OF_FIRST_CAT:
                controller.set_next_page_nbr(GET_PROD_FROM_A_SUBCAT_PAGE)
                return (controller.get_beverage_subcategories()[
                    choice - INDEX_OF_FIRST_CAT])

        elif page_nbr == GET_PROD_FROM_A_SUBCAT_PAGE:
            controller.manage_menu_header(choice)
            if choice in [NEXT_PRODUCTS, PREVIOUS_PRODUCTS]:
                controller.set_next_page_nbr(GET_PROD_FROM_A_SUBCAT_PAGE)

            elif choice >= INDEX_OF_FIRST_PROD:
                controller.set_next_page_nbr(DETAILS_OF_A_BEVERAGE_PROD_PAGE)

                return (controller.get_list_of_prods()[
                    choice - INDEX_OF_FIRST_PROD])
        else:
            controller.home_page()
