from db.db_creator import Product
from constants import (
    FAVORITE_SUBSTITUTE_DELETED,
    FAVORITES_PAGE,
    FAVS_FOR_A_PRODUCT,
    INDEX_OF_FIRST_PROD,
    LIST_OF_SUBSTITUTES_FOR_1_PRODUCT)


class FavoritesController:
    """analyse events on the favorites branch"""

    def analyze(self, controller, page_nbr, choice):
        """analyse events on the favorites branch"""
        if page_nbr == FAVORITES_PAGE:
            controller.manage_menu_header(choice)
            if choice >= INDEX_OF_FIRST_PROD:
                controller.set_next_page_nbr(LIST_OF_SUBSTITUTES_FOR_1_PRODUCT)
                controller.memory["chosen_pair"] = (
                    controller.memory["list_of_pairs__original_v_substitutes"][
                        choice - INDEX_OF_FIRST_PROD])

        elif page_nbr == FAVS_FOR_A_PRODUCT:
            controller.manage_menu_header(choice)
            if choice >= INDEX_OF_FIRST_PROD:
                controller.set_next_page_nbr(FAVORITE_SUBSTITUTE_DELETED)
                original_prod = (
                    controller
                    .memory["chosen_pair"][0])

                substitute_prod = (
                    controller
                    .memory["chosen_pair"][1]
                    [choice - INDEX_OF_FIRST_PROD])

                Product.delete_fav_substitute(original_prod, substitute_prod)

        else:
            controller.home_page()

