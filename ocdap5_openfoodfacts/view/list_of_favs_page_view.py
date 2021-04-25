import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    FAVORITES,
    FAVS_FOR_A_PRODUCT,
    ERROR_COLOR,
    INDEX_OF_FIRST_PROD)


class ListOfFavsPageView:
    """Display the page of all the favorite substitutes of a product """

    def show(
            self,
            memory,
            event_handler,
            clear_page_and_print_title,
            menu_header):

        clear_page_and_print_title(FAVS_FOR_A_PRODUCT)
        ic()
        print()
        print(f"Produit d'origine: {memory['chosen_pair'][0]}", end=" ")
        print(f"Marque: {memory['chosen_pair'][0].list_of_brands}")

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
Ou supprimer un favori ?
""")

        products = memory['chosen_pair'][1]
        for i, product_obj in enumerate(products):
            row_nbr = i + INDEX_OF_FIRST_PROD
            print(f"[{row_nbr}]", end=" ")
            print(f"{product_obj.product_name} | Marque:", end=" ")
            print(str([brand.brand_name
                       for brand in product_obj.list_of_brands]))
            print(f"Ingrédients: {product_obj.ingredients}")
            print(f"Plus d'infos: {product_obj.url}")
            print("________________________________________________________")
        print()

        choice = input(": ")
        try:
            choice = int(choice)
            event_handler(
                FAVORITES,
                FAVS_FOR_A_PRODUCT,
                choice)
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
                clear_page_and_print_title,
                menu_header,
                get_beverage_cat_index)
