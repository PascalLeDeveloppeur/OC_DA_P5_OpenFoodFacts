import sys

from icecream import ic

from constants import (
    CHOOSE_A_CATEGORY,
    SUBSTITUTE)


class SubstitueABeveragePageView:
    """Display the << baverage or food >> page"""

    def __init__(self):
        pass

    def show(self,
             controller_beverage_categories,
             event_handler,
             print_title,
             menu_header):
        print_title(CHOOSE_A_CATEGORY)

        print(f"""
Souhaitez-vous naviguer ?
{menu_header}
Ou choisir une catégorie ?
""")
        for i, category in enumerate(controller_beverage_categories):
            print(f"[{i + 4}] {category}")
        choice = input(": ")
        try:
            choice = int(choice)
            event_handler(SUBSTITUTE, "BEVERAGE_OR_FOOD", choice)
        except Exception:
            self.show(event_handler, print_title)
