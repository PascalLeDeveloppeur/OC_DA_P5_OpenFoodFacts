import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    ERROR_COLOR,
    FAVORITES,
    FAVORITES_PAGE,
    INDEX_OF_FIRST_PROD)


class FavoritesMainPageView:
    """Display the page of favorite products"""

    def show(
            self,
            memory,
            event_handler,
            clear_page_and_print_title,
            menu_header):

        clear_page_and_print_title(FAVORITES)
        ic()
        print()

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
Ou modifier une paire (original vs favori) ?
""")
        pairs = memory["list_of_pairs__original_v_substitutes"]

        for i, one_pair in enumerate(pairs):

            print()
            print(f"[{i + INDEX_OF_FIRST_PROD}] ")
            print(one_pair[0], end=" ")
            print(f"marque: {one_pair[0].list_of_brands}")

            print("est remplacé par: ")
            print(one_pair[1])
            print("-------------------------------------")

        choice = input(": ")
        try:
            choice = int(choice)

            event_handler(
                FAVORITES,
                FAVORITES_PAGE,
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
                memory,
                event_handler,
                clear_page_and_print_title,
                menu_header)
