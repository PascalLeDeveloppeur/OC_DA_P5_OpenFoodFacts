import sys

from constants import (
    CREATE_DB_PAGE,
    HOME_PAGE,
    INITIAL_PAGE)


class StarterController:
    """analyse events on the starter branch"""

    def __init__(self):
        pass

    def analyze(self, controller, page_nbr, choice, **kwargs):
        if page_nbr == INITIAL_PAGE:
            if choice == 1:
                controller.set_next_page_nbr(CREATE_DB_PAGE)
            elif choice == 2:
                controller.set_next_page_nbr(HOME_PAGE)
            elif choice == 3:
                print()
                print("Au revoir !")
                print()
                sys.exit()
            else:
                controller.set_next_page_nbr(INITIAL_PAGE)

        else:
            controller.home_page()
