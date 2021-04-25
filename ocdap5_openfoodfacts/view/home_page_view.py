from icecream import ic

from constants import (
    HOME,
    HOME_PAGE,
    TRUNK_BRANCH)


class HomePageView:
    """Display the home page"""

    

    def show(self, event_handler, clear_page_and_print_title):
        clear_page_and_print_title(HOME)
        ic()
        choice = input("""
Que souhaitez-vous faire ?

[1] Susbstituer une boisson par une autre de meilleure qualité
[2] Susbstituer un aliment par un autre de meilleure qualité
[3] Voir mes aliments de substitution préférés
[4] Quitter l'application
:""")
        try:
            choice = int(choice)
            event_handler(TRUNK_BRANCH, HOME_PAGE, choice)
        except Exception:
            self.show(event_handler, clear_page_and_print_title)
