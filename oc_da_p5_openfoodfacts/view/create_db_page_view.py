from constants import (
    CREATE_DB,
    CREATE_DB_PAGE,
    ROOT_BRANCH,
)


class CreateDbPageView:
    """Display the Create DB page"""

    def __init__(self):
        pass

    def show(self, event_handler, print_title):
        print_title(CREATE_DB)
        choice = input("""
Voulez-vous vraiment réinitialiser toute la base de données ?

[1] Oui
[2] Non
[3] Quitter l'application
:""")
        try:
            choice = int(choice)
            event_handler(ROOT_BRANCH, CREATE_DB_PAGE, choice)
        except Exception:
            self.show(event_handler, print_title)
