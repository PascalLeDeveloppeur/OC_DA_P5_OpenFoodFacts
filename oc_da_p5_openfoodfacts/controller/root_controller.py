import sys
import time

from icecream import ic

from db.db_creator import (
    Base,
    Category,
    engine,
    Product,
    # Shop,
    )
from model.data_downloader import DataDownloader
from model.data_formatter import DataFormatter

from constants import (
    DB_HAS_BEEN_CREATED,
    CREATE_DB_PAGE,
    SUBSTITUTE_PAGE,
)


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
                    Base.metadata.create_all(engine)
                    print("Tables créées.")

                    print("Filtrage et formattage des données en cours...")
                    prefiltered_products, categories, stores =\
                        self.__data_formatter.format_data(
                                    self.__rough_products)

                    # Fill database
                    print("Remplissage des tables en cours...")
                    Category.fill_database(categories)
                    print(" - Table category remplie.")
                    # Shop.fill_database(stores)
                    # print(" - Table shop remplie")
                    Product.fill_database(prefiltered_products,
                                          categories,
                                          stores)
                    sys.exit(ic())
                    controller.set_next_page_nbr(DB_HAS_BEEN_CREATED)
                except Exception as e:
                    print("Unable to drop nor create the database")
                    print(str(e))
                    time.sleep(10)
                    sys.exit(ic())

# request.requestexception

            elif choice == 2:
                controller.set_next_page_nbr(SUBSTITUTE_PAGE)
            elif choice == 3:
                print()
                print("Au revoir !")
                print()
                sys.exit()
            else:
                controller.create_db_page()

        if page_nbr == DB_HAS_BEEN_CREATED:
            if choice == 1:
                try:
                    print()
                    Base.metadata.drop_all(engine)
                    time.sleep(3)
                    Base.metadata.create_all(engine)
                    controller.set_next_page_nbr(DB_HAS_BEEN_CREATED)
                except Exception as e:
                    print("Unable to drop nor create the database")
                    print(str(e))
                    time.sleep(10)
                    sys.exit(ic())

            elif choice == 2:
                controller.set_next_page_nbr(SUBSTITUTE_PAGE)
            elif choice == 3:
                print()
                print("Au revoir !")
                print()
                sys.exit()
            else:
                controller.create_db_page()

        else:
            controller.home_page()
