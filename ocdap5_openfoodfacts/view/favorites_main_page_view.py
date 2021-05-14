import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CHOICE_ERROR,
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
        print()

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
""")
        pairs = memory["list_of_pairs__original_v_substitutes"]
        if pairs:
            print("Ou modifier une paire (original vs favori ?")
        else:
            print("Il n'y a pas encore de produit favori")
            print()
            print("Votre choix ?")

        # Set last_index to INDEX_OF_FIRST_PROD in order to
        # avoid error if there is no pairs
        last_index = INDEX_OF_FIRST_PROD  # ()
        for i, one_pair in enumerate(pairs):

            print()
            last_index = i + INDEX_OF_FIRST_PROD
            print(f"[{last_index}] ")
            print(one_pair[0], end=" ")
            print(f"marque: {one_pair[0].list_of_brands}")

            print("est remplacé par: ")
            print(one_pair[1])
            print("-------------------------------------")

        choice = input(": ")
        try:
            choice = int(choice)

            if choice > last_index:
                choice = CHOICE_ERROR

            event_handler(
                FAVORITES,
                FAVORITES_PAGE,
                choice)
        except ValueError:
            event_handler(
                FAVORITES,
                FAVORITES_PAGE,
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
            self.show(
                memory,
                event_handler,
                clear_page_and_print_title,
                menu_header)
