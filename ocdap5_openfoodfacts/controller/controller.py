import os
import sys
import time

from dotenv import load_dotenv
import traceback
from icecream import ic
from unidecode import unidecode
from pprint import pprint
from sqlalchemy.exc import (
    DBAPIError,
    InterfaceError)

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
    NORMAL_COLOR,
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

    def get_next_page(self):
        """Returns the number of the next page to be displayed.

        Returns:
            integer: Number of the next page to be displayed
        """
        return self.__next_page_nbr

    def set_next_page_nbr(self, next_page):
        """Set the number of the next page to be displayed.

        Args:
            next_page (integer): Number of the next page to be displayed.
        """
        self.__next_page_nbr = next_page

    def get_beverage_subcategories(self):
        """Returns a list of names of the subcategories that belong to the
        Beverages category.

        Returns:
            List of strings: Names of the subcategories that belong to the
            Beverages category.
        """
        return self.__beverages_subcategories

    def set_beverages_subcategories(self, beverage_subcategories):
        """Set a list of names of the subcategories that belong to the
        Beverages category.

        Args:
            beverage_subcategories (list of strings): list of subcategories
            that belong to the Beverages category.
        """
        self.__beverages_subcategories = beverage_subcategories

    def get_food_subcategories(self):
        """Returns a list of names of the subcategories that belong to the
        Food category.

        Returns:
            List of strings: Names of the subcategories that belong to the
            Food category.
        """
        return self.__food_subcategories

    def set_food_subcategories(self, food_subcategories):
        """Set a list of names of the subcategories that belong to the
        Food category.

        Args:
            food_subcategories (list of strings): list of subcategories
            that belong to the Food category.
        """
        self.__food_subcategories = food_subcategories

    def remove_accent(self, string):
        """Take Unicode data and try to represent it in ASCII characters
        (US keyboard)

        Args:
            string (string): Text to get modified.

        Returns:
            string: Modified text.
        """
        return unidecode(string)

    def run(self):
        """Run the application by calling the very first page.
        """
        self.__view.initial_page(self.event_handler)

    def event_handler(self, branch_name, page_nbr, choice, *args):
        """Analyzes the choice made by the user.

        Args:
            branch_name (integer): The number of the branch where the user
            is located.
            page_nbr (integer): The number of the page where the user is
            located.
            choice (integer): The choice made by the user.
        """
        if branch_name == FAVORITES:
            self.__favorites_controller.analyze(self,
                                                page_nbr,
                                                choice,
                                                *args)
        elif branch_name == ROOT_BRANCH:
            self.__root_controller.analyze(self,
                                           page_nbr,
                                           choice,
                                           *args)
        elif branch_name == STARTER:
            self.__starter_controller.analyze(self,
                                              page_nbr,
                                              choice,
                                              *args)
        elif branch_name == SUBSTITUTE:
            self.__substitute_controller.analyze(
                self, page_nbr, choice, *args)

        elif branch_name == TRUNK_BRANCH:
            self.__trunk_controller.analyze(self,
                                            page_nbr,
                                            choice,
                                            *args)
        else:
            self.home_page()

        self.__router.go_to(self)

    def go_to_previous_page(self):
        """Go to the previous page via the router.
        """
        self.__next_page_nbr = self.__next_page_nbr - 1
        self.__router.go_to(self)

    def is_empty(self, items_list):
        """Check if a list is empty.

        Args:
            items_list (list): List to get verified

        Returns:
            Boolean: True if the list is empty or else False.
        """
        return not items_list

    def manage_menu_header(self, choice):
        """Analyze the choice made by the user.
        This part checks if the user wants to go to the main menu,
        to the previous page or if he wants to leave the application.

        Args:
            choice (integer): Choice of the user.
        """
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
        """Call the view in order to display the create database page.
        """
        self.__view.create_db_page(self.event_handler)

    def db_created_page(self):
        """Call the view in order to display the page that indicate the
        database has been created.
        """
        self.__view.db_created_page(self.event_handler)

    def home_page(self):
        """Update the food and beverage list, then call the view, which
        in turn will call the main menu page.
        """
        try:
            if self.is_empty(self.__beverages_subcategories):
                self.set_beverages_subcategories(
                    Category.get_beverages_list())

            if self.is_empty(self.__food_subcategories):
                self.set_food_subcategories(
                    Category.get_food_list())

            self.__view.home_page(self.event_handler)
        except InterfaceError:  # Unable to connect to the database
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            Error!
            Unable to access the database.
            Maybe the database server did not start
            or the connection elements are not correct.
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())

        except DBAPIError:  # <= any database error
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            Error!
            Unable to drop nor create the database
            Something went wrong with the database.
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            Unable to drop nor create the database
            {str(e)}
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())

    def substitute_a_food(self):
        """Call the main view which in turn will call the view that will display
        the page when the user wants to substitute a food.
        """
        self.__view.substitute_a_food_page(
            self.memory,
            self.__food_subcategories,
            self.event_handler)

    def substitute_a_beverage(self, **kwargs):
        """Call the main view which in turn will call the view that will display
        the page when the user wants to substitute a beverage.
        """
        self.__view.substitute_a_beverage_page(self.memory,
                                               self.__beverages_subcategories,
                                               self.event_handler)

    def get_prod_from_a_food(self):
        """Store in memory a list of products in order to be used if the user
        go back to a previous page.
        Then call the view which in turn will call the view that will display
        the page when the user wants to get a product which is a food.
        """
        self.memory['list_of_products'] = list(
            Product.get_products_from_subcategory(
                FOOD,
                self.memory["subcategory_name"]))

        self.__view.get_prod_from_a_food_page(
            self.memory,
            self.event_handler)

    def get_prod_from_a_beverage(self):
        """Store in memory a list of products in order to be used if the user
        go back to a previous page.
        Then call the main view which in turn will call the view that will
        display the page when the user wants to get a product which is a
        beverage.
        """
        self.memory['list_of_products'] = list(
            Product.get_products_from_subcategory(
                BEVERAGES,
                self.memory["subcategory_name"]))

        self.__view.get_prod_from_a_beverage_page(
            self.memory,
            self.event_handler)

    def details_of_a_food_prod(self):
        """Call the main view which in turn will call the view that will display
        the page when the user wants to see the details of a product which is a
        food.
        """
        self.__view.details_of_a_food_prod_page(
            self.memory,
            self.event_handler)

    def details_of_a_beverage_prod(self):
        """Call the main view which in turn will call the view that will display
        the page when the user wants to see the details of a product which is a
        beverage.
        """
        self.__view.details_of_a_beverage_prod_page(
            self.memory,
            self.event_handler)

    def get_a_better_food(self):
        """Call the main view which in turn will call the view that will display
        the page when the user wants to see a list of better food.
        """
        self.__view.get_a_better_food(
            self.memory,
            self.event_handler)

    def get_a_better_beverage(self):
        """Call the main view which in turn will call the view that will display
        the page when the user wants to see a list of better beverages.
        """
        self.__view.get_a_better_beverage(
            self.memory,
            self.event_handler)

    def added_to_fav_food(self):
        """Call the main view which in turn will call the view that will display
        the page when a food has been add to the favorite substitutes.
        """
        self.__view.added_to_fav_food(self.event_handler)

    def added_to_fav(self):
        """Call the main view which in turn will call the view that will display
        the page when a beverage has been add to the favorite substitutes.
        """
        self.__view.added_to_fav(self.event_handler)

    def favorites_page(self, **kwargs):
        """Store the favorite products in memory then call the main view which
        in turn will call the view that will display the page when the user
        wants to see his favorite products.
        """
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
        """Call the main view which in turn will call the view that will display
        the page when the user wants to see the favorite substitutes of one
        product.
        """
        self.__view.list_of_favs(self.memory,
                                 self.event_handler)

    def one_fav_deleted(self):
        """Call the main view which in turn will call the view that will display
        the page that indicates a substitute has been deleted.
        """
        self.__view.one_fav_deleted(self.event_handler)
