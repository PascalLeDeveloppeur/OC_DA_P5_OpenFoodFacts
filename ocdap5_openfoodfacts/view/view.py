import os
import sys
import platform
import time

from icecream import ic

from logger import logger
from view.initial_page_view import InitialPageView
from view.home_page_view import HomePageView
from view.substitute_a_beverage_page_view import SubstituteABeveragePageView
from view.substitute_a_food_page_view import SubstituteAFoodPageView
from view.create_db_page_view import CreateDbPageView
from view.db_created_page_view import DbCreatedPageView
from view.get_prod_from_a_food_page_view import (
    GetProdFromAFoodPageView)

from view.get_prod_from_a_beverage_page_view import (
    GetProdFromABeveragePageView)

from view.details_of_a_food_prod_page_view import (
    DetailsOfAFoodProdPageView)

from view.details_of_a_beverage_prod_page_view import (
    DetailsOfABeverageProdPageView)

from view.get_a_better_food_page_view import GetABetterFoodPageView
from view.get_a_better_beverage_page_view import GetABetterBeveragePageView
from view.added_to_fav_food_page_view import AddedToFavFoodPageView
from view.added_to_fav_page_view import AddedToFavPageView
from view.favorites_main_page_view import FavoritesMainPageView
from view.list_of_favs_page_view import ListOfFavsPageView
from view.one_fav_deleted_page_view import OneFavDeletedPageView


class View:
    """Manage views"""

    def __init__(self):
        self.__beverage_cat_index = 0
        self.__beverage_prod_index = 0
        self.__food_cat_index = 0
        self.__food_prod_index = 0
        self.__initial_page_view = InitialPageView()
        self.__home_page_view = HomePageView()
        self.__favorites_page_view = FavoritesMainPageView()
        self.__added_to_fav_page_view = AddedToFavPageView()
        self.__added_to_fav_food_page_view = AddedToFavFoodPageView()
        self.__substitute_a_food_page_view = SubstituteAFoodPageView()
        self.__substitute_a_beverage_page_view = SubstituteABeveragePageView()
        self.__get_prod_from_a_beverage_page_view = (
            GetProdFromABeveragePageView())

        self.__get_prod_from_a_food_page_view = (
            GetProdFromAFoodPageView())

        self.__details_of_a_food_prod_page_view = (
            DetailsOfAFoodProdPageView)

        self.__details_of_a_beverage_prod_page_view = (
            DetailsOfABeverageProdPageView)

        self.__get_a_better_food_page_view = GetABetterFoodPageView()
        self.__get_a_better_beverage_page_view = GetABetterBeveragePageView()
        self.__create_db_page_view = CreateDbPageView()
        self.__db_created_page_view = DbCreatedPageView()
        self.__list_of_favs_page_view = ListOfFavsPageView()
        self.__one_fav_deleted_page_view = OneFavDeletedPageView()
        self.menu_header = """
[1] Aller à l'accueil
[2] Page précédente
[3] Quitter l'application

"""

    def clear_screen(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def get_food_cat_index(self):
        return self.__food_cat_index

    def set_food_cat_index(self, new_value):
        self.__food_cat_index = new_value

    def get_beverage_cat_index(self):
        return self.__beverage_cat_index

    def set_beverage_cat_index(self, new_value):
        self.__beverage_cat_index = new_value

    def get_beverage_prod_index(self):
        return self.__beverage_prod_index

    def set_beverage_prod_index(self, new_value):
        self.__beverage_prod_index = new_value

    def get_food_prod_index(self):
        return self.__beverage_prod_index

    def set_food_prod_index(self, new_value):
        self.__beverage_prod_index = new_value

    def clear_page_and_print_title(self, title):
        self.clear_screen()
        print(f"""{title}
              """)

    def initial_page(self, event_handler):
        self.__initial_page_view.show(event_handler,
                                      self.clear_page_and_print_title)

    def create_db_page(self, event_handler):
        self.__create_db_page_view.show(event_handler,
                                        self.clear_page_and_print_title)

    def db_created_page(self, event_handler):
        self.__db_created_page_view.show(event_handler,
                                         self.clear_page_and_print_title)

    def home_page(self, event_handler):
        self.__home_page_view.show(event_handler,
                                   self.clear_page_and_print_title)

    def substitute_a_food_page(self,
                               memory,
                               controller_categories,
                               event_handler):
        self.__substitute_a_food_page_view.show(
            memory,
            controller_categories,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header,
            self.__food_cat_index,
            self.set_food_cat_index)

    def substitute_a_beverage_page(self,
                                   memory,
                                   controller_categories,
                                   event_handler):

        self.__substitute_a_beverage_page_view.show(
            memory,
            controller_categories,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header,
            self.__beverage_cat_index,
            self.set_beverage_cat_index)

    def get_prod_from_a_food_page(self,
                                  memory,
                                  event_handler):
        self.__get_prod_from_a_food_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header,
            self.__food_prod_index,
            self.set_food_prod_index)

    def get_prod_from_a_beverage_page(self,
                                    memory,
                                    event_handler):
        self.__get_prod_from_a_beverage_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header,
            self.__beverage_prod_index,
            self.set_beverage_prod_index)

    def details_of_a_food_prod_page(self,
                                    memory,
                                    event_handler):

        self.__details_of_a_food_prod_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def details_of_a_beverage_prod_page(self,
                                        memory,
                                        event_handler):

        self.__details_of_a_beverage_prod_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def get_a_better_food(self,
                          memory,
                          event_handler):

        self.__get_a_better_food_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def get_a_better_beverage(self,
                              memory,
                              event_handler):

        self.__get_a_better_beverage_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def added_to_fav_food(self,
                          event_handler):

        self.__added_to_fav_food_page_view.show(
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def added_to_fav(self, event_handler):

        self.__added_to_fav_page_view.show(
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def favorites_page(self,
                       memory,
                       event_handler):

        self.__favorites_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def list_of_favs(self,
                     memory,
                     event_handler):

        self.__list_of_favs_page_view.show(
            memory,
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)

    def one_fav_deleted(self, event_handler):
        self.__one_fav_deleted_page_view.show(
            event_handler,
            self.clear_page_and_print_title,
            self.menu_header)