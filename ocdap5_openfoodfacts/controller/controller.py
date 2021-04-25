import os
import sys
import time

from dotenv import load_dotenv
import traceback
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
    ERROR_COLOR,
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
        self.__subcategory = None
        self.__product = None
        self.__router = Router()
        self.__view = View()
        self.__starter_controller = StarterController()
        self.__substitute_controller = SubstituteController()
        self.__favorites_controller = FavoritesController()
        self.__trunk_controller = TrunkController()
        self.__root_controller = RootController()
        self.memory = {"best_products": None,
                       "chosen_pair": None,
                       "fav_prod": None,
                       "list_of_pairs__original_v_substitutes": None,
                       "list_of_products": None,
                       "product": None,
                       "subcategory_name": None,
                       "substitute_product": None}

    def get_list_of_prods(self):
        return self.__list_of_prods

    def set_list_of_prods(self, list_of_prods):
        self.__list_of_prods = list_of_prods

    def get_product(self):
        return self.__product

    def set_product(self, product):
        self.__product = product

    def get_subcategory(self):
        return self.__subcategory

    def set_subcategory(self, subcategory):
        self.__subcategory = subcategory

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
            self.__substitute_controller.analyze(
                self, page_nbr, choice, *args)
            ic()
            time.sleep(3)

        elif branch_nbr == TRUNK_BRANCH:
            self.__trunk_controller.analyze(self,
                                            page_nbr,
                                            choice,
                                            *args)
        else:
            self.home_page()

        self.__router.go_to(self)

    def go_to_previous_page(self, **kwargs):
        print("page: ", self.__next_page_nbr)
        self.__next_page_nbr = self.__next_page_nbr - 1
        print("page: ", self.__next_page_nbr)
        time.sleep(2)
        self.__router.go_to(self, **kwargs)

    def get_categories_from(self, element):
        return Category.extract_beverage_category(self)

    def is_empty(self, items_list):
        return not items_list

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
        self.__view.substitute_a_food_page(
            self.memory,
            self.__food_subcategories,
            self.event_handler)

    def substitute_a_beverage(self, **kwargs):
        self.__view.substitute_a_beverage_page(self.memory,
                                               self.__beverages_subcategories,
                                               self.event_handler)

    def get_prod_from_a_food(self):
        self.memory['list_of_products'] = list(
            Product.get_products_from_subcategory(
                FOOD,
                self.memory["subcategory_name"]))

        self.__view.get_prod_from_a_food_page(
            self.memory,
            self.event_handler)

    def get_prod_from_a_beverage(self):
        self.memory['list_of_products'] = list(
            Product.get_products_from_subcategory(
                BEVERAGES,
                self.memory["subcategory_name"]))

        self.__view.get_prod_from_a_beverage_page(
            self.memory,
            self.event_handler)

    def details_of_a_food_prod(self):
        self.__view.details_of_a_food_prod_page(
            self.memory,
            self.event_handler)

    def details_of_a_beverage_prod(self):
        self.__view.details_of_a_beverage_prod_page(
            self.memory,
            self.event_handler)

    def get_a_better_food(self):
        self.__view.get_a_better_food(
            self.memory,
            self.event_handler)

    def get_a_better_beverage(self):
        self.__view.get_a_better_beverage(
            self.memory,
            self.event_handler)

    def added_to_fav_food(self):
        self.__view.added_to_fav_food(self.event_handler)

    def added_to_fav(self):
        self.__view.added_to_fav(self.event_handler)

    def favorites_page(self, **kwargs):
        try:
            self.memory["list_of_pairs__original_v_substitutes"] = (
                Product.get_favorites())

            self.__view.favorites_page(
                self.memory,
                self.event_handler)
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}""")
            sys.exit(ic())

    def list_of_favs(self):
        self.__view.list_of_favs(self.memory,
                                 self.event_handler)

    def one_fav_deleted(self):
        self.__view.one_fav_deleted(self.event_handler)
