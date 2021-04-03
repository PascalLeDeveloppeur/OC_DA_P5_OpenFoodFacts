from constants import (
    HOME,
    HOME_PAGE,
    TRUNK_BRANCH)


class HomePageView:
    """Display the home page"""

    def __init__(self):
        pass

    def show(self, event_handler, print_title):
        print_title(HOME)
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
            self.show(event_handler, print_title)
