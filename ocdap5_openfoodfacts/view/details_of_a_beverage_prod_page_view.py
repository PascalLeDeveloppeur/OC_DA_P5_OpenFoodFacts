import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CHOICE_ERROR,
    ERROR_COLOR,
    DETAILS_OF_A_BEVERAGE_PROD_PAGE,
    PRODUCT_DETAILS,
    SUBSTITUTE)


class DetailsOfABeverageProdPageView:
    """Display the page of the details of a product which is a beverage"""

    def show(
            memory,
            event_handler,
            clear_page_and_print_title,
            menu_header):

        clear_page_and_print_title(PRODUCT_DETAILS)
        subcategory_name = memory["subcategory_name"]
        product = memory["product"]
        print()
        print(subcategory_name)
        print()
        print(product.product_name, end=" ")
        print(" | Nutriscore: ", product.nutriscore, end=" | Marque: ")
        # Below, str form is possible because of __repr__ in Product class
        print(product.list_of_brands)
        print()
        print("Description: ", product.description)
        print()
        print("Ingrédients: ", product.ingredients)
        print()
        print("Lieu(x) de ventes:", end=" ")
        list_of_stores = ", ".join(
            store.store_name for store in product.list_of_stores)
        print(list_of_stores)
        print()
        print("Plus d'info: ", product.url)
        print()

        print(
            f"""
Que souhaitez-vous faire ?
{menu_header}[4] Chercher un produit équivalent de meilleure qualité ?
""")

        choice = input(": ")
        try:
            choice = int(choice)

            event_handler(
                SUBSTITUTE,
                DETAILS_OF_A_BEVERAGE_PROD_PAGE,
                choice)
        except ValueError:
            event_handler(
                SUBSTITUTE,
                DETAILS_OF_A_BEVERAGE_PROD_PAGE,
                CHOICE_ERROR)
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}""")
            sys.exit(ic())
