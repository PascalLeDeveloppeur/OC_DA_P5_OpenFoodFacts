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
    """Display the page that list the best substitute food"""

    def __init__(self):
        pass

    def show(self,
             memory,
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
                controller_food_categories,
                event_handler,
                clear_page_and_print_title,
                menu_header,
                get_food_cat_index)
