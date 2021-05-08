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
    ERROR_COLOR,
    HOME_PAGE,
    INITIAL_PAGE,
    NORMAL_COLOR,
    PROGRAM_QUIT_BY_USER)
from logger import logger


class RootController:
    """analyse events on the root branch"""

    def __init__(self):
        self.__datadownloader = DataDownloader()
        self.__data_formatter = DataFormatter()
        self.__rough_products = []

    def analyze(self, controller, page_nbr, choice):
        if page_nbr == CREATE_DB_PAGE:
            if choice == 1:
                try:
                    logger.info(
                        "Suppression de la base de données en cours...")
                    Base.metadata.drop_all(engine)
                    logger.info("Base de données supprimée.")

                    logger.info("Téléchargement des produits depuis "
                                + "Open Food Facts en cours...")
                    self.__rough_products = self.__datadownloader.download()
                    logger.info(f"{len(self.__rough_products)}"
                                + " produits bruts ont été téléchargés")

                    logger.info("Création de la base de données en cours...")
                    logger.info("Création des tables en cours...")
                    Base.metadata.create_all(engine)
                    logger.info("Tables créées.")

                    logger.info(
                        "Filtrage et formattage des données en cours...")
                    prefiltered_products = (self.__data_formatter
                                            .prefilter_products(
                                                self.__rough_products))

                    brands, categories, products, stores = (
                        self.__data_formatter.format_products(
                                        controller,
                                        prefiltered_products))
                    # Database feeding
                    logger.info("Remplissage des tables en cours...")
                    Brand.fill_database(brands)
                    logger.info(" - Table brand remplie.")
                    Category.fill_database(categories)
                    logger.info(" - Table category remplie.")
                    Store.fill_database(stores)
                    logger.info(" - Table store remplie.")
                    Product.fill_database(products,
                                          brands,
                                          categories,
                                          stores)
                    logger.info(" - Table product remplie.")
                    logger.info(" - Tables d'associations remplies.")
                    logger.info("Récupération des sous-catégories"
                                + "de [Boissons] et [Aliments] en cours...")
                    Category.extract_beverage_subcategories(controller)

                    Category.set_beverages_that_are_food_too()
                    Category.remove_food_categories_from_beverages()

                    controller.set_beverages_subcategories(
                        Category.get_beverages_list())

                    controller.set_food_subcategories(
                        Category.get_food_list())

                    logger.info(
                        "Sous-catégories de [Boissons]"
                        + "et [Aliments]récupérées")
                    controller.set_next_page_nbr(DB_HAS_BEEN_CREATED)
                except InterfaceError:  # Unable to connect to the database
                    e_traceback = traceback.format_exc()
                    logger.error(f"""
                    {ERROR_COLOR}
                    ******************************************
                    {e_traceback}
                    ******************************************
                    Error!
                    Unable to drop nor create the database
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
            elif choice == 2:
                controller.set_next_page_nbr(HOME_PAGE)

            elif choice == 3:
                logger.info(F"""
                {PROGRAM_QUIT_BY_USER}
                """)
                sys.exit()
            else:
                controller.create_db_page()

        elif page_nbr == DB_HAS_BEEN_CREATED:
            controller.set_next_page_nbr(INITIAL_PAGE)
