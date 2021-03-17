import os
import platform

from view.initial_page_view import InitialPageView
from view.home_page_view import HomePageView
from view.baverage_or_food_page_view import BaverageOrFoodPageView
from view.create_db_page_view import CreateDbPageView
from view.db_created_page_view import DbCreatedPageView


class View:
    """Manage views"""

    def __init__(self):
        self.__initial_page_view = InitialPageView()
        self.__home_page_view = HomePageView()
        self.__beverage_or_food_page_view = BaverageOrFoodPageView()
        self.__create_db_page_view = CreateDbPageView()
        self.__db_created_page_view = DbCreatedPageView()
        self.menu_header = """
[1] Aller à l'accueil
[2] Page précédente
[3] Quitter l'application

"""

    def print_title(self, title):
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
                                      self.print_title)

    def create_db_page(self, event_handler):
        self.__create_db_page_view.show(event_handler,
                                        self.print_title)

    def db_created_page(self, event_handler):
        self.__db_created_page_view.show(event_handler,
                                        self.print_title)

    def home_page(self, event_handler):
        self.__home_page_view.show(event_handler,
                                   self.print_title)

    def beverage_or_food_page(self, event_handler):
        self.__beverage_or_food_page_view.show(event_handler,
                                               self.print_title,
                                               self.menu_header)

    def clear_screen(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
