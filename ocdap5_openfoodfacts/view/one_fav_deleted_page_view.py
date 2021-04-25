import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    DELETED_FROM_FAV,
    ERROR_COLOR,
    FAVORITES,
    FAVORITE_SUBSTITUTE_DELETED)


class OneFavDeletedPageView:
    """Display the page that confirm the deletion of product from fav list"""

    def show(self,
             event_handler,
             clear_page_and_print_title,
             menu_header):

        clear_page_and_print_title(DELETED_FROM_FAV)
        ic()
        print()
        print("Que souhaitez-vous faire ?")
        print(f"{menu_header}")
        choice = input(": ")

        try:
            choice = int(choice)

            event_handler(
                FAVORITES,
                FAVORITE_SUBSTITUTE_DELETED,
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
