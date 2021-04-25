from constants import (
    DATABASE_CREATED,
    DB_HAS_BEEN_CREATED,
    ROOT_BRANCH)


class DbCreatedPageView:
    """Display the page that say Database has been created"""

    

    def show(self, event_handler, clear_page_and_print_title):
        clear_page_and_print_title(DATABASE_CREATED)
        choice = input("""
La base de données à bien été crée.
Appuyez sur [Entrée] pour continuer
:""")
        try:
            choice = None
            event_handler(ROOT_BRANCH, DB_HAS_BEEN_CREATED, choice)
        except Exception:
            self.show(event_handler, clear_page_and_print_title)
