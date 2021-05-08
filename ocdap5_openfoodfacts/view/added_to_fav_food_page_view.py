import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    ADDED_TO_FAV_FOOD,
    ERROR_COLOR,
    GET_A_BETTER_FOOD_PAGE,
    SUBSTITUTE)


class AddedToFavFoodPageView:
    """Display the page that confirm the addition of product in the fav list"""

    def show(self,
             event_handler,
             clear_page_and_print_title,
             menu_header):

        clear_page_and_print_title(ADDED_TO_FAV_FOOD)
        ic()
        print()
        print("Que souhaitez-vous faire ?")
        print(f"{menu_header}")
        choice = input(": ")

        try:
            choice = int(choice)

            event_handler(
                SUBSTITUTE,
                GET_A_BETTER_FOOD_PAGE,
                choice,)
        except IndexError:
            pass
        except ValueError:
            pass
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}""")
            sys.exit(ic())
