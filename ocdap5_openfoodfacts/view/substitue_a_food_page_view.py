import sys

from constants import (
    CHOOSE_A_CATEGORY,
    SUBSTITUTE)


class SubstitueAFoodPageView:
    """Display the << baverage or food >> page"""

    def __init__(self):
        pass

    def show(self, event_handler, print_title, menu_header):
        print_title(CHOOSE_A_CATEGORY)
        
        choice = input(f"""
Que souhaitez-vous faire ?
{menu_header}
[4] Remplacer une boisson
[5] Remplacer un aliment
:""")
        try:
            choice = int(choice)
            event_handler(SUBSTITUTE, "BEVERAGE_OR_FOOD", choice)
        except Exception:
            self.show(event_handler, print_title)