import sys

from icecream import ic

from constants import (
    CREATE_DB_PAGE,
    DB_HAS_BEEN_CREATED,
    HOME_PAGE,
    INITIAL_PAGE,
    SUBSTITUTE_A_BEVERAGE,
    SUBSTITUTE_A_FOOD)


class Router:
    """Take user to wanted page"""

    def __init__(self):
        pass

    def go_to(self, controller, **kwargs):
        next_page = controller.get_next_page()

        # Branch: starter
        if next_page == INITIAL_PAGE:
            controller.run()
        elif next_page == CREATE_DB_PAGE:
            controller.create_db_page()
        elif next_page == HOME_PAGE:
            controller.home_page()

        # Branch: Substitute a beverage
        elif next_page == SUBSTITUTE_A_BEVERAGE:
            controller.substitute_a_beverage(**kwargs)

        # Branch: Substitute a food
        elif next_page == SUBSTITUTE_A_FOOD:
            controller.substitute_a_food(**kwargs)

        # Branch: Watch my fav
        elif next_page == 301:
            controller.favorites_page(**kwargs)
        elif next_page == 302:
            controller.fav_product_page(**kwargs)

        # Branch: root db creator
        elif next_page == DB_HAS_BEEN_CREATED:
            controller.db_created_page(**kwargs)

        # Home page
        else:
            controller.home_page()
