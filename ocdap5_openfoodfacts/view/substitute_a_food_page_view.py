import sys

from icecream import ic
import traceback

from logger import logger
from constants import (
    CHOICE_ERROR,
    CHOOSE_A_CATEGORY,
    ERROR_COLOR,
    INDEX_OF_FIRST_CAT,
    NBR_OF_CATEGORIES,
    NEXT_CATEGORIES,
    PREVIOUS_CATEGORIES,
    SUBSTITUTE,
    SUBSTITUTE_A_FOOD_PAGE)


class SubstituteAFoodPageView:
    """Display the << subcategories of food >> page"""

    def show(
            self,
            memory,
            controller_food_categories,
            event_handler,
            clear_page_and_print_title,
            menu_header,
            get_food_cat_index,
            set_food_cat_index):

        clear_page_and_print_title(CHOOSE_A_CATEGORY)

        print(
            f"""
Souhaitez-vous naviguer ?
{menu_header}
Ou choisir une catégorie ?
""")
        is_next_cat_displayed = False
        is_previous_cat_displayed = False
        for i, category in enumerate(
            controller_food_categories[get_food_cat_index:(
                    get_food_cat_index + NBR_OF_CATEGORIES)]):

            index_of_category = i + get_food_cat_index + INDEX_OF_FIRST_CAT
            print(f"[{index_of_category}] {category}")
        print()
        if get_food_cat_index > 0:
            print(f"[{PREVIOUS_CATEGORIES}] Catégories précédentes")
            is_previous_cat_displayed = True

        if get_food_cat_index + NBR_OF_CATEGORIES < (
                len(controller_food_categories) - 1):
            print(f"[{NEXT_CATEGORIES}] Catégories suivantes")
            is_next_cat_displayed = True

        choice = input(": ")
        try:
            choice = int(choice)
            if choice == NEXT_CATEGORIES and is_next_cat_displayed:
                set_food_cat_index(
                    get_food_cat_index + NBR_OF_CATEGORIES)
            elif choice == PREVIOUS_CATEGORIES and is_previous_cat_displayed:
                set_food_cat_index(
                    get_food_cat_index - NBR_OF_CATEGORIES)
            elif choice > index_of_category:
                choice = CHOICE_ERROR

            event_handler(
                SUBSTITUTE,
                SUBSTITUTE_A_FOOD_PAGE,
                choice)
        except ValueError:
            event_handler(
                SUBSTITUTE,
                SUBSTITUTE_A_FOOD_PAGE,
                CHOICE_ERROR)
        except IndexError:
            event_handler(
                SUBSTITUTE,
                SUBSTITUTE_A_FOOD_PAGE,
                CHOICE_ERROR)
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}""")
            sys.exit(ic())
            self.show(
                controller_food_categories,
                event_handler,
                clear_page_and_print_title,
                menu_header,
                get_food_cat_index)
