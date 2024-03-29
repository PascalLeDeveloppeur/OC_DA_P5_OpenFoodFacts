import sys

from icecream import ic

from logger import logger
from constants import (
    FAVORITES_PAGE,
    HOME_PAGE,
    PROGRAM_QUIT_BY_USER,
    SUBSTITUTE_A_BEVERAGE_PAGE,
    SUBSTITUTE_A_FOOD_PAGE)


class TrunkController:
    """analyse events on the main branch"""

    def analyze(self, controller, page_nbr, choice):
        """analyse events on the main branch"""
        if page_nbr == HOME_PAGE:
            if choice == 1:
                controller.set_next_page_nbr(SUBSTITUTE_A_BEVERAGE_PAGE)
            elif choice == 2:
                controller.set_next_page_nbr(SUBSTITUTE_A_FOOD_PAGE)
            elif choice == 3:
                controller.set_next_page_nbr(FAVORITES_PAGE)
            elif choice == 4:
                logger.info(F"""
                {PROGRAM_QUIT_BY_USER}
                """)
                sys.exit()
            else:
                controller.home_page()

        else:
            controller.home_page()
