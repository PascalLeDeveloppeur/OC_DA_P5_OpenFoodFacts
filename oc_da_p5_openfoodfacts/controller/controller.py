import os
import sys

from dotenv import load_dotenv
from icecream import ic

from controller.starter_controller import StarterController
from controller.substitute_controller import SubstituteController
from controller.favorites_controller import FavoritesController
from controller.trunk_controller import TrunkController
from controller.root_controller import RootController
from router.router import Router
from view.view import View
from constants import (
    FAVORITES,
    INITIAL_PAGE,
    ROOT_BRANCH,
    STARTER,
    SUBSTITUTE,
    TRUNK_BRANCH,
)


class Controller:

    def __init__(self):
        load_dotenv()
        self.__branch_nbr = STARTER
        self.__page_nbr = INITIAL_PAGE
        self.__next_page_nbr = 0
        self.__router = Router()
        self.__view = View()
        self.__starter_controller = StarterController()
        self.__substitute_controller = SubstituteController()
        self.__favorites_controller = FavoritesController()
        self.__trunk_controller = TrunkController()
        self.__root_controller = RootController()

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

    def run(self):
        self.__view.initial_page(self.event_handler)

    def event_handler(self, branch_nbr, page_nbr, choice, **kwargs):
        if branch_nbr == FAVORITES:
            self.__favorites_controller.analyze(self,
                                                page_nbr,
                                                choice,
                                                **kwargs)
        elif branch_nbr == ROOT_BRANCH:
            self.__root_controller.analyze(self,
                                           page_nbr,
                                           choice,
                                           **kwargs)
        elif branch_nbr == STARTER:
            self.__starter_controller.analyze(self,
                                              page_nbr,
                                              choice,
                                              **kwargs)
        elif branch_nbr == SUBSTITUTE:
            self.__substitute_controller.analyze(self,
                                                 page_nbr,
                                                 choice,
                                                 **kwargs)
        elif branch_nbr == TRUNK_BRANCH:
            self.__trunk_controller.analyze(self,
                                            page_nbr,
                                            choice,
                                            **kwargs)
        else:
            self.home_page()

        self.__router.go_to(self)

    def go_to_previous_page(self, **kwargs):
        self.__next_page_nbr = self.__page_nbr - 1
        self.__router.go_to(self, **kwargs)

    def create_db_page(self):
        self.__view.create_db_page(self.event_handler)
        """
Je dois:
1 - Supprimer la bdd si elle existe ------------------------------- Done
2 - Créer la bdd ---------------------------------------------------Done
3 - Récupérer des données de chez Open Food Facts
4 - Filtrer les données
5 - Raccourcir les noms trop longs (product, category, shop)
6 - Formater les données
7 - Remplir la bdd
8 - Aller à la page d'accueil
"""
        sys.exit()

    def db_created_page(self):
        self.__view.db_created_page(self.event_handler)

    def home_page(self):
        self.__view.home_page(self.event_handler)

    def substitute_page(self, **kwargs):
        self.__view.beverage_or_food_page(self.event_handler)
        print("Branche substituer un aliment page 1")
        sys.exit()
        # choice = input(PRIMARY_MENU)
