import sys

from constants import (
    CREATE_DB_PAGE,
    DB_HAS_BEEN_CREATED,
    HOME_PAGE,
    INITIAL_PAGE,
    SUBSTITUTE_PAGE,
)


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

        # Branch: Substitute
        elif next_page == SUBSTITUTE_PAGE:
            controller.substitute_page(**kwargs)
        elif next_page == 102:
            controller.category_page(**kwargs)
        elif next_page == 103:
            controller.product_page(**kwargs)

        # Branch: Watch my fav
        elif next_page == 201:
            controller.favorites_page(**kwargs)
        elif next_page == 202:
            controller.fav_product_page(**kwargs)

        # Branch: root db creator
        elif next_page == DB_HAS_BEEN_CREATED:
            controller.db_created_page(**kwargs)

        # Home page
        else:
            controller.home_page()
