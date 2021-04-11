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
        print(" | Nutriscore: ", product.nutriscore, end=" | Marque: ")
        # Below, str form is possible because of __repr__ in Product class
        print(product.list_of_brands)
        print()

        print("Que souhaitez-vous faire ?")
        print(f"{menu_header}")
        if best_products:
            print("Ou Ajouter un produit en favori ?")
            print()
            for i, pair in enumerate(best_products):
                product = pair[0]
                print(f"[{INDEX_OF_FIRST_PROD + i}] {product}", end=" | ")
                print(f"Nutriscore: {product.nutriscore}", end=" | ")
                print(f"Marque: {product.list_of_brands}")
                print(f"            Ingrédients: {product.ingredients}")
                print(f"            Lieux de vente: {product.list_of_stores}")
                print("_______________________________")
                print()
        else:
            print("Il n'y a pas de produit de substitution pour cet", end=" ")
            print("article dans la base de données !")
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
