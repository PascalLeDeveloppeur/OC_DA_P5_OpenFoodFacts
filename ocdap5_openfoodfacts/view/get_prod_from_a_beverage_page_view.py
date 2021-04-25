import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CHOOSE_A_PRODUCT,
    ERROR_COLOR,
    GET_PROD_FROM_A_BEVERAGE_PAGE,
    INDEX_OF_FIRST_PROD,
    NBR_OF_PRODUCTS,
    NEXT_PRODUCTS,
    PREVIOUS_PRODUCTS,
    SUBSTITUTE)


class GetProdFromABeveragePageView:
    """Display the page of all the products of a
    << subcategory of beverages >> """

    

    def show(
            self,
            memory,
            event_handler,
            clear_page_and_print_title,
            menu_header,
            get_beverage_prod_index,
            set_beverage_prod_index):

        clear_page_and_print_title(CHOOSE_A_PRODUCT)
        ic()
        print()
        print(memory["subcategory_name"])

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
Ou choisir un produit ?
""")
        is_next_prod_displayed = False
        is_previous_prod_displayed = False

        products = memory["list_of_products"]
        for i, product_obj in enumerate(
            products[get_beverage_prod_index:(
                    get_beverage_prod_index + NBR_OF_PRODUCTS)]):

            index_of_product = (
                i + get_beverage_prod_index + INDEX_OF_FIRST_PROD)

            print(f"[{index_of_product}] {product_obj.product_name} | Marque: "
                  + str([brand.brand_name
                         for brand in product_obj.list_of_brands]))
        print()
        if get_beverage_prod_index > 0:
            print(f"[{PREVIOUS_PRODUCTS}] Produits précédents")
            is_previous_prod_displayed = True

        if get_beverage_prod_index + NBR_OF_PRODUCTS < (
                len(products) - 1):
            print(f"[{NEXT_PRODUCTS}] Produits suivants")
            is_next_prod_displayed = True

        choice = input(": ")
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
                GET_PROD_FROM_A_BEVERAGE_PAGE,
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
