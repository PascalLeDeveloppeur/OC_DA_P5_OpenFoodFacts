import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    ERROR_COLOR,
    HOME,
    HOME_PAGE,
    NORMAL_COLOR,
    TRUNK_BRANCH)


class HomePageView:
    """Display the home page"""

    def show(self, event_handler, clear_page_and_print_title):
        clear_page_and_print_title(HOME)
        choice = input("""
Que souhaitez-vous faire ?

[1] Susbstituer une boisson par une autre de meilleure qualité
[2] Susbstituer un aliment par un autre de meilleure qualité
[3] Voir mes aliments de substitution préférés
[4] Quitter l'application
:""")
        try:
            choice = int(choice)
            print()
            print("Patientez un instant ...")
            event_handler(TRUNK_BRANCH, HOME_PAGE, choice)
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

