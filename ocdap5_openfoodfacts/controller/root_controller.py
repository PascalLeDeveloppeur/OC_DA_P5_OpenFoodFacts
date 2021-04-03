import sys
import time
import traceback

from sqlalchemy.exc import (
    DBAPIError,
    InterfaceError)
from icecream import ic
from pprint import pprint

from db.db_creator import (
    Base,
    Brand,
    Category,
    engine,
    Product,
    Store)
from model.data_downloader import DataDownloader
from model.data_formatter import DataFormatter

from constants import (
    CREATE_DB_PAGE,
    DB_HAS_BEEN_CREATED,
    HOME_PAGE,
    INITIAL_PAGE)


class RootController:
    """analyse events on the root branch"""

    def __init__(self):
        self.__datadownloader = DataDownloader()
        self.__data_formatter = DataFormatter()
        self.__rough_products = []

    def analyze(self, controller, page_nbr, choice, **kwargs):
        if page_nbr == CREATE_DB_PAGE:
            if choice == 1:
                try:
                    print()
                    print("Suppression de la base de données en cours...")
                    Base.metadata.drop_all(engine)
                    print("Base de données supprimée.")

                    print("Téléchargement des produits depuis "
                          + "Open Food Facts en cours...")
                    self.__rough_products = self.__datadownloader.download()
                    print(f"{len(self.__rough_products)}"
                          + " produits bruts ont été téléchargés")

                    print("Création de la base de données en cours...")
                    print("Création des tables en cours...")
                    Base.metadata.create_all(engine)
                    print("Tables créées.")

                    print("Filtrage et formattage des données en cours...")
                    prefiltered_products = (self.__data_formatter
                                            .prefilter_products(
                                                self.__rough_products))

                    brands, categories, products, stores = (
                        self.__data_formatter.format_products(
                                        controller,
                                        prefiltered_products))

                    # Database feeding
                    print("Remplissage des tables en cours...")
                    Brand.fill_database(brands)
                    print(" - Table brand remplie.")
                    Category.fill_database(categories)
                    print(" - Table category remplie.")
                    Store.fill_database(stores)
                    print(" - Table store remplie.")
                    Product.fill_database(products,
                                          brands,
                                          categories,
                                          stores)
                    print(" - Table product remplie.")
                    print(" - Tables d'associations remplies.")
                    print(len(self.__rough_products) - len(products),
                          " produits ont été rejetés pour non-conformité.")
                    print("Récupération des sous-catégories", end=" ")
                    print("de [Boissons] et [Aliments] en cours...")
                    Category.extract_beverage_subcategories(controller)

                    controller.set_beverage_subcategories(
                        Category.get_beverages_list())

                    controller.set_food_subcategories(
                        Category.get_food_list())

                    print("Sous-catégories de [Boissons] et", end=" ")
                    print("[Aliments]récupérées.")
                    sys.exit(ic())
                    time.sleep(3)
                    controller.set_next_page_nbr(DB_HAS_BEEN_CREATED)
                except InterfaceError:  # Unable to connect to the database
                    e_traceback = traceback.format_exc()
                    print(e_traceback)
                    print("**********************************************")
                    print("Error!")
                    print("Unable to drop nor create the database")
                    print("Maybe the database server did not start")
                    print("or the connection elements are not correct.")
                    print("**********************************************")
                    time.sleep(2)
                    sys.exit(ic())

                except DBAPIError:  # <= any database error
                    e_traceback = traceback.format_exc()
                    print(e_traceback)
                    print("**********************************************")
                    print("Error!")
                    print("Unable to drop nor create the database")
                    print("Something went wrong with the database.")
                    print("**********************************************")
                    time.sleep(2)
                    sys.exit(ic())
                except Exception as e:
                    e_traceback = traceback.format_exc()
                    print(e_traceback)
                    print("**********************************************")
                    print("Unable to drop nor create the database")
                    print(str(e))
                    print("**********************************************")
                    time.sleep(2)
                    sys.exit(ic())

            elif choice == 2:
                controller.set_next_page_nbr(HOME_PAGE)

            elif choice == 3:
                print()
                print("Au revoir !")
                print()
                sys.exit()
            else:
                controller.create_db_page()

        elif page_nbr == DB_HAS_BEEN_CREATED:
            controller.set_next_page_nbr(INITIAL_PAGE)
