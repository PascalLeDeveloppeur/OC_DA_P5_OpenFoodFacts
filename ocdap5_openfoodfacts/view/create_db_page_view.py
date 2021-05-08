import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CREATE_DB,
    CREATE_DB_PAGE,
    ERROR_COLOR,
    NORMAL_COLOR,
    ROOT_BRANCH)


class CreateDbPageView:
    """Display the Create DB page"""

    def show(self, event_handler, clear_page_and_print_title):
        clear_page_and_print_title(CREATE_DB)
        choice = input("""
Voulez-vous vraiment réinitialiser toute la base de données ?

[1] Oui
[2] Non
[3] Quitter l'application
:""")
        try:
            choice = int(choice)
            event_handler(ROOT_BRANCH, CREATE_DB_PAGE, choice)
        except ValueError:
            self.show(event_handler, clear_page_and_print_title)
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            Unable to drop nor create the database
            {str(e)}
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())
