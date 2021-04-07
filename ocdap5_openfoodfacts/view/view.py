import os
import sys
import platform

from icecream import ic

from view.initial_page_view import InitialPageView
from view.home_page_view import HomePageView
from view.substitue_a_beverage_page_view import SubstitueABeveragePageView
from view.substitue_a_food_page_view import SubstitueAFoodPageView
from view.create_db_page_view import CreateDbPageView
from view.db_created_page_view import DbCreatedPageView
from view.get_prod_from_a_subcat_page_view import GetProdFromASubcatPageView
from view.details_of_a_beverage_prod_page_view import DetailsOfABeverageProdPageView


class View:
    """Manage views"""

    def __init__(self):
        self.__beverage_cat_index = 0
        self.__beverage_prod_index = 0
        self.__initial_page_view = InitialPageView()
        self.__home_page_view = HomePageView()
        self.__substitue_a_beverage_page_view = SubstitueABeveragePageView()
        self.__get_prod_from_a_subcat_page_view = GetProdFromASubcatPageView()
        self.__details_of_a_beverage_prod_page_view = (
            DetailsOfABeverageProdPageView)
        self.__substitue_a_food_page_view = SubstitueAFoodPageView()
        self.__create_db_page_view = CreateDbPageView()
        self.__db_created_page_view = DbCreatedPageView()
        self.menu_header = """
[1] Aller à l'accueil
[2] Page précédente
[3] Quitter l'application

"""

    def get_beverage_cat_index(self):
        return self.__beverage_cat_index

    def set_beverage_cat_index(self, new_value):
        self.__beverage_cat_index = new_value

    def get_beverage_prod_index(self):
        return self.__beverage_prod_index

    def set_beverage_prod_index(self, new_value):
        self.__beverage_prod_index = new_value

    def clear_and_print_title(self, title):
        self.clear_screen()
        print(f"""{title}
              """)

    def chek_if_menu_header_choosen(self, choice, **kwargs):
        """This is the 1st part of each menu except the starter branch menu."""
        if choice == 1:
            self.home_page()
        if choice == 2:
            self.go_to_previous_page(**kwargs)

    def initial_page(self, event_handler):
        self.__initial_page_view.show(event_handler,
                                      self.clear_and_print_title)

    def create_db_page(self, event_handler):
        self.__create_db_page_view.show(event_handler,
                                        self.clear_and_print_title)

    def db_created_page(self, event_handler):
        self.__db_created_page_view.show(event_handler,
                                         self.clear_and_print_title)

    def home_page(self, event_handler):
        self.__home_page_view.show(event_handler,
                                   self.clear_and_print_title)

    def substitue_a_beverage_page(self,
                                  controller_categories,
                                  event_handler):
        self.__substitue_a_beverage_page_view.show(
            controller_categories,
            event_handler,
            self.clear_and_print_title,
            self.menu_header,
            self.__beverage_cat_index,
            self.set_beverage_cat_index)

    def get_prod_from_a_subcat_page(self,
                                    subcategory_name,
                                    products,
                                    event_handler):
        self.__get_prod_from_a_subcat_page_view.show(
            subcategory_name,
            products,
            event_handler,
            self.clear_and_print_title,
            self.menu_header,
            self.__beverage_prod_index,
            self.set_beverage_prod_index)

    def details_of_a_beverage_prod_page(self,
                                    #  subcategory_name,
                                    product,
                                    event_handler):
        self.__details_of_a_beverage_prod_page_view.show(
            # subcategory_name,
            product,
            event_handler,
            self.clear_and_print_title,
            self.menu_header,
            self.__beverage_prod_index,
            self.set_beverage_prod_index)

    def substitue_a_food_page(self, event_handler):
        self.__substitue_a_food_page_view.show(event_handler,
                                               self.clear_and_print_title,
                                               self.menu_header)

    def clear_screen(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
