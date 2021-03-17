import sys

from constants import (
    FAVORITES_PAGE,
    HOME_PAGE,
    SUBSTITUTE_PAGE,
)


class TrunkController:
    """analyse events on the main branch"""

    def __init__(self):
        pass

    def analyze(self, controller, page_nbr, choice, **kwargs):
        if page_nbr == HOME_PAGE:
            if choice == 1:
                controller.set_next_page_nbr(SUBSTITUTE_PAGE)
            elif choice == 2:
                controller.set_next_page_nbr(FAVORITES_PAGE)
            elif choice == 3:
                print()
                print("Au revoir !")
                print()
                sys.exit()
            else:
                controller.home_page()

        else:
            controller.home_page()
