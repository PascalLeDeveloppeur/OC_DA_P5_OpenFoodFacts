import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    EN_BEVERAGES,
    CHOICE_ERROR,
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
        print()
        print(memory["subcategory_name"])

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
""")
        is_next_prod_displayed = False
        is_previous_prod_displayed = False

        products = memory["list_of_products"]
        index_of_product = INDEX_OF_FIRST_PROD
        has_some_products = (products[get_beverage_prod_index:(
                    get_beverage_prod_index + NBR_OF_PRODUCTS)])

        if has_some_products:
            print("Ou choisir un produit ?")
        else:
            print("Hélas, il n'y a pas de boisson dans cette catégorie")

        for i, product_obj in enumerate(
            products[get_beverage_prod_index:(
                    get_beverage_prod_index + NBR_OF_PRODUCTS)]):

            if product_obj.main_group == EN_BEVERAGES:
                index_of_product = (
                    i + get_beverage_prod_index + INDEX_OF_FIRST_PROD)

                print(f"[{index_of_product}]"
                      f" {product_obj.product_name} | Marque: "
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
            elif choice > index_of_product or (
                    not has_some_products and choice > 3):
                choice = CHOICE_ERROR

            event_handler(
                SUBSTITUTE,
                GET_PROD_FROM_A_BEVERAGE_PAGE,
                choice)
        except IndexError:
            event_handler(
                SUBSTITUTE,
                GET_PROD_FROM_A_BEVERAGE_PAGE,
                CHOICE_ERROR)
        except ValueError:
            event_handler(
                SUBSTITUTE,
                GET_PROD_FROM_A_BEVERAGE_PAGE,
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
