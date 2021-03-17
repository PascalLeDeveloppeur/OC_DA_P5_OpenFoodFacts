from constants import (
    HOME_PAGE,
)


class FavoritesController:
    """analyse events on the favorites branch"""

    def __init__(self):
        pass

    def analyze(self, controller, page_nbr, choice, **kwargs):
        if page_nbr == HOME_PAGE:
            if choice == 2:
                controller.set_next_page_nbr(201)

        else:
            self.home_page()
