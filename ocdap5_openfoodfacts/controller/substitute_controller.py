import sys
import time

from icecream import ic

from db.db_creator import (Product)
from constants import (
    ADD_TO_FAV_PAGE,
    DETAILS_OF_A_BEVERAGE_PROD_PAGE,
    GET_A_BETTER_BEVERAGE_PAGE,
    GET_PROD_FROM_A_SUBCAT_PAGE,
    INDEX_OF_FIRST_CAT,
    INDEX_OF_FIRST_PROD,
    LOOK_FOR_A_BETTER_PRODUCT,
    MAX_PRODS_DISPLAYED,
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
            # logger.info("SUBSTITUTE_A_BEVERAGE_PAGE")
            # logger.info(ic())
            # time.sleep(2)
            controller.manage_menu_header(choice)
            if choice in [NEXT_CATEGORIES, PREVIOUS_CATEGORIES]:
                controller.set_next_page_nbr(SUBSTITUTE_A_BEVERAGE_PAGE)

            elif choice >= INDEX_OF_FIRST_CAT:
                controller.set_next_page_nbr(GET_PROD_FROM_A_SUBCAT_PAGE)
                controller.memory["subcategory_name"] = (
                    controller.get_beverage_subcategories()[
                        choice - INDEX_OF_FIRST_CAT])

        elif page_nbr == GET_PROD_FROM_A_SUBCAT_PAGE:
            # logger.info("GET_PROD_FROM_A_SUBCAT_PAGE")
            # logger.info(ic())
            # time.sleep(2)
            controller.manage_menu_header(choice)
            if choice in [NEXT_PRODUCTS, PREVIOUS_PRODUCTS]:
                controller.set_next_page_nbr(GET_PROD_FROM_A_SUBCAT_PAGE)

            elif choice >= INDEX_OF_FIRST_PROD:
                controller.set_next_page_nbr(DETAILS_OF_A_BEVERAGE_PROD_PAGE)

                controller.memory["product"] = (
                    controller.memory["list_of_products"][
                        choice - INDEX_OF_FIRST_PROD])

        elif page_nbr == DETAILS_OF_A_BEVERAGE_PROD_PAGE:
            # logger.info("DETAILS_OF_A_BEVERAGE_PROD_PAGE")
            # logger.info(ic())
            # logger.info("product = "
            #             + controller.memory["product"].product_name)
            # time.sleep(2)
            controller.manage_menu_header(choice)
            if choice == LOOK_FOR_A_BETTER_PRODUCT:
                controller.memory["best_products"] = (
                    Product.get_better_prods(
                        controller.memory["product"],
                        controller.memory["subcategory_name"]))
                controller.set_next_page_nbr(GET_A_BETTER_BEVERAGE_PAGE)

        elif page_nbr == GET_A_BETTER_BEVERAGE_PAGE:
            # logger.info("GET_A_BETTER_BEVERAGE_PAGE")
            # logger.info(ic())
            # time.sleep(2)
            controller.manage_menu_header(choice)
            if (choice >= INDEX_OF_FIRST_PROD
                    and (choice - INDEX_OF_FIRST_PROD) < MAX_PRODS_DISPLAYED):

                controller.memory["fav_prod"] = (
                    controller.memory["best_products"][
                        choice - INDEX_OF_FIRST_PROD][0])

                Product.add_favorite(
                    controller.memory["product"],
                    controller.memory["fav_prod"])

                controller.set_next_page_nbr(ADD_TO_FAV_PAGE)
                logger.info("Fin pour l'instant")
                sys.exit(ic())
        else:
            controller.home_page()
