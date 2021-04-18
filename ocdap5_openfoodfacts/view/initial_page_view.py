import sys

from icecream import ic

from constants import (
    STARTER,
    INITIAL_PAGE,
    INITIAL)


class InitialPageView:
    """Display the very first page of the application"""

    def __init__(self):
        pass

    def show(self, event_handler, clear_page_and_print_title):
        clear_page_and_print_title(INITIAL)
        ic()
        choice = input("""
Que souhaitez-vous faire ?

[1] Créer / Recréer la base de données locale
[2] Utiliser la base de donnée locale
[3] Quitter l'application
:""")
        try:
            choice = int(choice)
            event_handler(STARTER, INITIAL_PAGE, choice)
        except Exception:
            self.show(event_handler, clear_page_and_print_title)
