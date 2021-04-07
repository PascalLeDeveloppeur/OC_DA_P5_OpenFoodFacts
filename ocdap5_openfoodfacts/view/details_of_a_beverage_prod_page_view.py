import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CHOOSE_A_PRODUCT,
    ERROR_COLOR,
    GET_PROD_FROM_A_SUBCAT_PAGE,
    INDEX_OF_FIRST_PROD,
    NBR_OF_PRODUCTS,
    NEXT_PRODUCTS,
    PREVIOUS_PRODUCTS,
    SUBSTITUTE)


class DetailsOfABeverageProdPageView:
    """Display the page of the details of a product which is a beverage"""

    def __init__(self):
        pass

    def show(
            self,
            subcategory_name,
            product,
            event_handler,
            clear_and_print_title,
            menu_header,
            get_beverage_prod_index,
            set_beverage_prod_index):

        clear_and_print_title(CHOOSE_A_PRODUCT)
        print()
        print(subcategory_name)
        print()
        print(f"{product.product_name}  {str(product.list_of_brands)} ")
        print()
        print(f"Ingrédients: {product.ingredients}")
        print(f"Lieu(x) de ventes:  {str(product.stores)}")

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
Ou chercher un produit équivalent ?
""")

        choice = input(": ")
        sys.exit(ic())
        try:
            choice = int(choice)
            if choice == NEXT_PRODUCTS and is_next_prod_displayed:
                set_beverage_prod_index(
                    get_beverage_prod_index + NBR_OF_PRODUCTS)
            elif choice == PREVIOUS_PRODUCTS and is_previous_prod_displayed:
                set_beverage_prod_index(
                    get_beverage_prod_index - NBR_OF_PRODUCTS)

            event_handler(
                SUBSTITUTE,
                GET_PROD_FROM_A_SUBCAT_PAGE,
                choice,
                get_beverage_prod_index)
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}""")
            sys.exit(ic())
            self.show(
                controller_beverage_categories,
                event_handler,
                clear_and_print_title,
                menu_header,
                get_beverage_cat_index)
