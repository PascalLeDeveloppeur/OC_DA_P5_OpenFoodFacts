import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    ERROR_COLOR,
    STARTER,
    INITIAL_PAGE,
    INITIAL,
    NORMAL_COLOR)


class InitialPageView:
    """Display the very first page of the application"""

    def show(self, event_handler, clear_page_and_print_title):
        clear_page_and_print_title(INITIAL)
        choice = input("""
Que souhaitez-vous faire ?

[1] Créer / Recréer la base de données locale
[2] Utiliser la base de donnée locale
[3] Quitter l'application
:""")
        try:
            choice = int(choice)
            event_handler(STARTER, INITIAL_PAGE, choice)
        except ValueError:
            self.show(event_handler, clear_page_and_print_title)
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())
