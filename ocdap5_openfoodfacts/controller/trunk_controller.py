import sys

from icecream import ic

from constants import (
    FAVORITES_PAGE,
    HOME_PAGE,
    SUBSTITUTE_A_BEVERAGE,
    SUBSTITUTE_A_FOOD)


class TrunkController:
    """analyse events on the main branch"""

    def __init__(self):
        pass

    def analyze(self, controller, page_nbr, choice, **kwargs):
        if page_nbr == HOME_PAGE:
            if choice == 1:
                controller.set_next_page_nbr(SUBSTITUTE_A_BEVERAGE)
            elif choice == 2:
                controller.set_next_page_nbr(SUBSTITUTE_A_FOOD)
            elif choice == 3:
                controller.set_next_page_nbr(FAVORITES_PAGE)
            elif choice == 4:
                print()
                print("Au revoir !")
                print()
                sys.exit()
            else:
                controller.home_page()

        else:
            controller.home_page()
