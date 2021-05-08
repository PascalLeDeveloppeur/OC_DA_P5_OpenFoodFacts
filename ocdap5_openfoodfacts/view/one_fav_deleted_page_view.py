import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CHOICE_ERROR,
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
        print()
        print("Pressez la touche [Entrée]")
        input(": ")

        try:
            event_handler(
                FAVORITES,
                FAVORITE_SUBSTITUTE_DELETED,
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
