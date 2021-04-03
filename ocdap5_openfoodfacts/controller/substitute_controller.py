import sys

from constants import (
    SUBSTITUTE_A_BEVERAGE,
    SUBSTITUTE_A_FOOD)


class SubstituteController:
    """analyse events on the substitute branch"""

    def __init__(self):
        pass

    def analyze(self, controller, page_nbr, choice, **kwargs):
        if page_nbr == BEVERAGE_OR_FOOD:
            controller.manage_menu_header(choice)
            if choice == 4:
                self.set_next_page_nbr(SUBSTITUTE_A_BEVERAGE)

        else:
            controller.home_page()
