import os
import sys
import time

from dotenv import load_dotenv
from icecream import ic
from unidecode import unidecode
from pprint import pprint

from controller.starter_controller import StarterController
from controller.substitute_controller import SubstituteController
from controller.favorites_controller import FavoritesController
from controller.trunk_controller import TrunkController
from controller.root_controller import RootController
from router.router import Router
from view.view import View
from db.db_creator import (
    Base,
    Brand,
    Category,
    engine,
    Product,
    Store)
from constants import (
    BEVERAGES,
    FAVORITES,
    FOOD,
    HOME_PAGE,
    INITIAL_PAGE,
    PROGRAM_QUIT_BY_USER,
    ROOT_BRANCH,
    STARTER,
    SUBSTITUTE,
    TRUNK_BRANCH)
from logger import logger


class Controller:

    def __init__(self):
        load_dotenv()
        self.__branch_nbr = STARTER
        self.__page_nbr = INITIAL_PAGE
        self.__next_page_nbr = 0
        self.__beverages_subcategories = set()
        self.__food_subcategories = set()
        self.__list_of_prods = None
        self.__router = Router()
        self.__view = View()
        self.__starter_controller = StarterController()
        self.__substitute_controller = SubstituteController()
        self.__favorites_controller = FavoritesController()
        self.__trunk_controller = TrunkController()
        self.__root_controller = RootController()

    def get_list_of_prods(self):
        return self.__list_of_prods

    def set_list_of_prods(self, list_of_prods):
        self.__list_of_prods = list_of_prods

    def get_view(self):
        return self.__view

    def get_branch(self):
        return self.__branch_nbr

    def set_branch(self, branch):
        self.__branch_nbr = branch

    def get_page(self):
        return self.__page_nbr

    def set_page(self, page):
        self.__page_nbr = page

    def get_next_page(self):
        return self.__next_page_nbr

    def set_next_page_nbr(self, next_page):
        self.__next_page_nbr = next_page

    def get_beverage_subcategories(self):
        return self.__beverages_subcategories

    def set_beverages_subcategories(self, beverage_subcategories):
        self.__beverages_subcategories = beverage_subcategories

    def get_food_subcategories(self):
        return self.__food_subcategories

    def set_food_subcategories(self, food_subcategories):
        self.__food_subcategories = food_subcategories

    def remove_accent(self, string):
        return unidecode(string)

    def run(self):
        self.__view.initial_page(self.event_handler)

    def event_handler(self, branch_nbr, page_nbr, choice, *args):
        elt = {}
        if branch_nbr == FAVORITES:
            self.__favorites_controller.analyze(self,
                                                page_nbr,
                                                choice,
                                                *args)
        elif branch_nbr == ROOT_BRANCH:
            self.__root_controller.analyze(self,
                                           page_nbr,
                                           choice,
                                           *args)
        elif branch_nbr == STARTER:
            self.__starter_controller.analyze(self,
                                              page_nbr,
                                              choice,
                                              *args)
        elif branch_nbr == SUBSTITUTE:
            elt["subcategory_of_beverage"] = (
                self.__substitute_controller.analyze(
                        self, page_nbr, choice, *args))

        elif branch_nbr == TRUNK_BRANCH:
            self.__trunk_controller.analyze(self,
                                            page_nbr,
                                            choice,
                                            *args)
        else:
            self.home_page()

        self.__router.go_to(self, elt)

    def go_to_previous_page(self, **kwargs):
        print("page: ", self.__next_page_nbr)
        self.__next_page_nbr = self.__next_page_nbr - 1
        print("page: ", self.__next_page_nbr)
        time.sleep(5)
        self.__router.go_to(self, **kwargs)

    def manage_menu_header(self, choice):
        if choice == 1:
            self.set_next_page_nbr(HOME_PAGE)
        elif choice == 2:
            self.go_to_previous_page()
        elif choice == 3:
            logger.info(F"""
            {PROGRAM_QUIT_BY_USER}
            """)
            sys.exit()

    def create_db_page(self):
        self.__view.create_db_page(self.event_handler)

    def db_created_page(self):
        self.__view.db_created_page(self.event_handler)

    def home_page(self):
        if self.is_empty(self.__beverages_subcategories):
            self.set_beverages_subcategories(
                Category.get_beverages_list())

        if self.is_empty(self.__food_subcategories):
            self.set_food_subcategories(
                Category.get_food_list())

        self.__view.home_page(self.event_handler)

    def substitute_a_food(self, **kwargs):
        self.__view.substitue_a_food_page(self.event_handler)
        logger.info("Branche substituer un aliment page 1")
        sys.exit()

    def substitute_a_beverage(self, **kwargs):
        logger.info(ic())
        time.sleep(3)
        self.__view.substitue_a_beverage_page(self.__beverages_subcategories,
                                              self.event_handler)

    def get_prod_from_a_subcat(self, subcategory_of_beverage):
        self.__list_of_prods = list(
            Product.get_products_from_subcategory(
                BEVERAGES,
                subcategory_of_beverage))

        self.__view.get_prod_from_a_subcat_page(
            subcategory_of_beverage,
            self.__list_of_prods,
            self.event_handler)

    def details_of_a_beverage_prod(self, product):
        self.__view.details_of_a_beverage_prod_page(
            product,
            self.event_handler)

    def get_categories_from(self, element):
        return Category.extract_beverage_category(self)

    def is_empty(self, items_list):
        return not items_list
