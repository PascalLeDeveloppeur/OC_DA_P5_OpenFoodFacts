import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    BETTER_BEVERAGES,
    ERROR_COLOR,
    GET_A_BETTER_BEVERAGE_PAGE,
    INDEX_OF_FIRST_PROD,
    SUBSTITUTE)


class GetABetterBeveragePageView:
    """Display the page that list the best substitute beverages"""

    def __init__(self):
        pass

    def show(self,
             memory,
             event_handler,
             clear_and_print_title,
             menu_header):

        clear_and_print_title(BETTER_BEVERAGES)
        subcategory_name = memory["subcategory_name"]
        product = memory["product"]
        best_products = memory["best_products"]
        print()
        print(subcategory_name)
        print()
        print("Produit à remplacer: ", product.product_name, end=" ")
        print(str([brand.brand_name for brand in product.list_of_brands]))
        print()

        print(
            f"""
Que souhaitez-vous faire ?
{menu_header}
Ou Ajouter un produit en favori
""")
        for i, pair in enumerate(best_products):
            product = pair[0]
            print(f"[{INDEX_OF_FIRST_PROD + i}] {product}", end=" | ")
            print(f"Nutriscore: {product.nutriscore}", end=" | ")
            print(f"Marque: {product.list_of_brands}")
            print(f"            Ingrédients: {product.ingredients}")
            print(f"            Lieux de vente: {product.list_of_stores}")
            print("_______________________________")
            print()
        print()
        choice = input(": ")
        try:
            choice = int(choice)

            event_handler(
                SUBSTITUTE,
                GET_A_BETTER_BEVERAGE_PAGE,
                choice,)
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
