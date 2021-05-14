import os
import sys
import time
from sqlalchemy.sql import elements

from unidecode import unidecode
from icecream import ic
import traceback
from pprint import pprint

from logger import logger
from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    desc,
    exists,
    exc,
    ForeignKey,
    func,
    Integer,
    String,
    Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.expression import true

from constants import (
    BEVERAGES,
    BRAND_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    EN_BEVERAGES,
    ERROR_COLOR,
    INGREDIENTS_MAX_LENGTH,
    LIST_OF_BEVERAGES_THAT_ARE_FOOD_TOO,
    LIST_OF_BEVERAGES_TO_REMOVE_FROM_FOOD,
    LIST_OF_FOOD_TO_REMOVE_FROM_BEVERAGE,
    LIST_OF_WRONG_BEVERAGES,
    MAX_PRODS_DISPLAYED,
    NORMAL_COLOR,
    PRODUCT_NAME_MAX_LENGTH,
    STORE_NAME_MAX_LENGTH,
    URL_MAX_LENGTH)

# Elements of connection to the database ====
load_dotenv()
DATABASE = os.getenv("DATABASE")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")

Base = declarative_base()

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}")

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Construction of the tables ====

# Association tables
l_category_and_product = Table(
    'l_category_product',
    Base.metadata,
    Column('fk_product_id', Integer, ForeignKey('product.id')),
    Column('fk_category_id', Integer, ForeignKey('category.category_id')))

l_product_and_store = Table(
    'l_product_store',
    Base.metadata,
    Column('fk_product_id', Integer, ForeignKey('product.id')),
    Column('fk_store_id', Integer, ForeignKey('store.store_id')))

l_brand_and_product = Table(
    'l_brand_product',
    Base.metadata,
    Column('fk_product_id', Integer, ForeignKey('product.id')),
    Column('fk_brand_id', Integer, ForeignKey('brand.brand_id')))

l_original_and_substitute = Table(
    'l_original_substitute',
    Base.metadata,
    Column('favorite_id', Integer, primary_key=True),
    Column('original_prod_id', Integer, ForeignKey('product.id')),
    Column('substitute_prod_id', Integer, ForeignKey('product.id')))


# Tables
class Brand(Base):
    """Table that contains the brands of the products
    """
    __tablename__ = 'brand'
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String(BRAND_NAME_MAX_LENGTH),
                        nullable=False,
                        unique=True)

    # List of products that can be found in a store
    list_of_products_made_by_the_brand = relationship(
        "Product",
        secondary=l_brand_and_product,
        back_populates="list_of_brands",
        cascade="all, delete",
        passive_deletes=True)

    def __str__(self):
        return self.brand_name.title()

    def __repr__(self):
        return self.brand_name.title()

    @classmethod
    def fill_database(cls, brands):
        """feed the table
        """
        for brand in brands:
            new_brand = Brand(brand_name=str(brand))
            session.add(new_brand)
            session.commit()


class Category(Base):
    """Table that contains the categories of the products
    """
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(CATEGORY_NAME_MAX_LENGTH),
                           nullable=False,
                           unique=True)
    is_beverage = Column(Boolean, default=False)
    is_food = Column(Boolean, default=False)

    # List of products that belong to a selected category
    list_of_products = relationship(
        "Product",
        secondary=l_category_and_product,
        back_populates="list_of_categories",
        cascade="all, delete",
        passive_deletes=True,
        lazy='joined')

    def __str__(self):
        return self.category_name.title()

    def __repr__(self):
        return self.category_name.title()

    @classmethod
    def fill_database(cls, categories):
        """feed the table
        """
        for category in categories:
            try:
                new_category = Category(category_name=category)
                session.add(new_category)
                session.commit()
            except exc.IntegrityError:
                session.rollback()

    @classmethod
    def set_beverage_subcategories(cls, controller):
        """Collect a list of subcategories that are part of
        the main category: Beverages.

        Here is the process:
        1. Select the " Beverages" category
        2. Select all products in this category
        3. For each of the selected products, select all the associated
            categories as they are necessarily part of "Beverages"
            and put them in the list of names <<beverage_categories_names>>.
        4. For each category whose name is in the list, update its
            <<is_beverage>> field. Set it to true."""
        beverage = (session.query(Category)
                    .filter(Category.category_name == BEVERAGES)
                    .one_or_none())
        if beverage:
            # Collecting products from the Beverage category.
            products_list = beverage.list_of_products
            products_list = cls.remove_wrong_beverages_from_list(products_list)
            beverage_categories_names = Product.get_categories_from_products(
                products_list)
            for beverage_category_name in beverage_categories_names:
                category = (
                    session.query(Category)
                    .filter(Category.category_name == beverage_category_name)
                    .one_or_none())
                category.is_beverage = True

            session.commit()
        else:
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            Error!
            No beverage found
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())

    @classmethod
    def set_food_subcategories(cls, controller):
        """Collect a list of subcategories that are not beverages.

        Here is the process:
        1. Select a list of products that are not beverages
        2. For each product from the list, select all the associated
            categories as they are necessarily part of "Food"
            and put them in the list of names <<food_categories_names>>.
        4. For each category whose name is in the list, update its
            <<is_food>> field. Set it to true."""
        products_that_are_not_beverages = Product.only_food_list()
        if products_that_are_not_beverages:
            food_categories_names = Product.get_categories_from_products(
                products_that_are_not_beverages)
            for food_category_name in food_categories_names:
                category = (
                    session.query(Category)
                    .filter(Category.category_name == food_category_name)
                    .one_or_none())
                category.is_food = True

            session.commit()
        else:
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            Error!
            No food found
            ******************************************
            {ic()} {NORMAL_COLOR}""")
            sys.exit(ic())

    @classmethod
    def remove_wrong_beverages_from_list(cls, products_list):
        """Remove products that are not beverage from the beverages list

        Args:
            products_list (list of objects): Initial list of beverages

        Returns:
            list of objects: Filtered list of beverages
        """
        return [
            prod for prod in products_list
            if prod.product_name not in LIST_OF_WRONG_BEVERAGES]

    @classmethod
    def get_beverages_list(cls):
        """Return from the database a list that contains the names of
        categories that are beverages.

        Returns:
            list of strings: beverages
        """
        beverages = (
            session.query(Category.category_name)
            .filter(Category.is_beverage == true())
            .all())
        beverages = [str(elt).strip("()',\"") for elt in beverages]
        beverages.sort()
        return beverages

    @classmethod
    def get_food_list(cls):
        """Return from the database a list that contains the names of
        categories that are food.

        Returns:
            list of strings: food
        """
        food_list = (
            session.query(Category.category_name)
            .filter(Category.is_food == true())
            .all())
        food_list = [str(elt).strip("()',\"") for elt in food_list]
        food_list.sort()
        return food_list

    @classmethod
    def set_beverages_that_are_food_too(cls):
        """For all categories that are both beverages and food, update the
        "Product" table of the database. Set the fields "is_beverage"
        and "is_food" to true.
        """
        for dual_cat in LIST_OF_BEVERAGES_THAT_ARE_FOOD_TOO:
            beverages_that_are_food = (
                session.query(Category)
                .filter(Category.category_name.like(f"{dual_cat}%"))
                .all())
            for category in beverages_that_are_food:
                category.is_beverage = True
                category.is_food = True
            session.commit()

    @classmethod
    def remove_food_categories_from_beverages(cls):
        """Unset products as beverages in the database because they are not.
        """
        for food_category in LIST_OF_FOOD_TO_REMOVE_FROM_BEVERAGE:
            categories = (
                session.query(Category)
                .filter(Category.category_name.like(f"{food_category}%"))
                .all())
            for category in categories:
                category.is_beverage = False
                category.is_food = True
            session.commit()

    @classmethod
    def remove_beverage_categories_from_food(cls):
        """Unset products as food in the database because they are not.
        """
        for beverage_category in LIST_OF_BEVERAGES_TO_REMOVE_FROM_FOOD:
            categories = (
                session.query(Category)
                .filter(Category.category_name.like(f"{beverage_category}%"))
                .all())
            for category in categories:
                category.is_beverage = True
                category.is_food = False
            session.commit()


class Store(Base):
    """Table that contains the stores where a product
    can be found.
    """
    __tablename__ = 'store'
    store_id = Column(Integer, primary_key=True)
    store_name = Column(String(STORE_NAME_MAX_LENGTH),
                        nullable=False,
                        unique=True)

    # List of products that can be found in a store
    list_of_products_in_a_store = relationship(
        "Product",
        secondary=l_product_and_store,
        back_populates="list_of_stores",
        cascade="all, delete",
        passive_deletes=True)

    def __str__(self):
        return self.store_name.title()

    def __repr__(self):
        return self.store_name.title()

    @classmethod
    def fill_database(cls, stores):
        """feed the table
        """
        for store in stores:
            new_store = Store(store_name=store)
            session.add(new_store)
            session.commit()


class Product(Base):
    """Table that contains all the products
    """
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(PRODUCT_NAME_MAX_LENGTH), nullable=False)
    main_group = Column(String(PRODUCT_NAME_MAX_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_MAX_LENGTH), nullable=False)
    nutriscore = Column(String(2), nullable=False)
    ingredients = Column(String(INGREDIENTS_MAX_LENGTH), nullable=False)
    url = Column(String(URL_MAX_LENGTH), nullable=False)

    # List of categories to which a product belongs
    list_of_categories = relationship(
        "Category",
        secondary=l_category_and_product,
        back_populates="list_of_products",
        cascade="all, delete",
        passive_deletes=True,
        lazy='joined')

    # List of stores where the product can be found
    list_of_stores = relationship(
        "Store",
        secondary=l_product_and_store,
        back_populates="list_of_products_in_a_store",
        cascade="all, delete",
        passive_deletes=True)

    # List of brands that make this product
    list_of_brands = relationship(
        "Brand",
        secondary=l_brand_and_product,
        back_populates="list_of_products_made_by_the_brand",
        cascade="all, delete",
        passive_deletes=True)

    # List of pairs (original product and substitute product)
    pairs = relationship(
        "Product",
        secondary=l_original_and_substitute,
        primaryjoin=id == l_original_and_substitute.c.original_prod_id,
        secondaryjoin=id == l_original_and_substitute.c.substitute_prod_id)

    # list of substitutes products for one original product
    all_substitutes = relationship(
        'Product',
        secondary=l_original_and_substitute,
        primaryjoin=id == l_original_and_substitute.c
        .original_prod_id,
        secondaryjoin=id == l_original_and_substitute.c
        .substitute_prod_id,
        backref='all_originals'
    )

    def __str__(self):
        return self.product_name.title()

    def __repr__(self):
        return self.product_name.title()

    @classmethod
    def fill_database(cls, products, brands, categories, stores):
        """Feed the table "Product" and its related association tables.

        Args:
            products (list): List of products coming from OpenFoodFacts
            brands (list): List of brands coming from OpenFoodFacts
            categories (list): List of categories coming from OpenFoodFacts
            stores (list): List of stores coming from OpenFoodFacts
        """
        for product in products:
            is_compliant = True
            ingredients_str = product.get("ingredients")
            if type(ingredients_str) != str:
                is_compliant = False
            ingredients_str = cls.rename_if_not_exists(ingredients_str)

            nutriscore_str = product.get("nutriscore_grade")
            nutriscore_str = cls.rename_if_not_exists(nutriscore_str)

            product_name_str = product.get("product_name")
            product_name_str = cls.rename_if_not_exists(product_name_str)

            product_main_group = product.get("pnns_groups_1")
            product_main_group = cls.rename_if_not_exists(product_main_group)

            description_str = product.get("description")
            description_str = cls.rename_if_not_exists(description_str)

            url_str = product.get("url")
            url_str = cls.rename_if_not_exists(url_str)
            if len(url_str) > URL_MAX_LENGTH:
                is_compliant = False

            is_commitable = False
            if is_compliant:
                # insert product
                new_product = Product(
                    product_name=product_name_str,
                    main_group=product_main_group,
                    description=description_str,
                    nutriscore=nutriscore_str,
                    ingredients=ingredients_str,
                    url=url_str)
                session.add(new_product)

                for brand in brands:
                    if brand in product.get("brands"):
                        row_brand = (
                            session.query(Brand)
                            .filter(Brand.brand_name == brand)
                            .one())

                        # add in association table
                        new_product.list_of_brands.append(row_brand)
                        is_commitable = True
                if is_commitable:
                    session.commit()
                else:
                    session.rollback()

                for category in categories:
                    if category in product.get("categories"):
                        row_category = (
                            session.query(Category)
                            .filter(Category.category_name == category)
                            .one())

                        # add in association table
                        new_product.list_of_categories.append(row_category)
                        is_commitable = True
                if is_commitable:
                    session.commit()
                else:
                    session.rollback()
                for store in stores:
                    if store in product.get("stores"):
                        row_store = (
                            session.query(Store)
                            .filter(Store.store_name == store)
                            .one())

                        # add in association table
                        new_product.list_of_stores.append(row_store)
                        is_commitable = True
                if is_commitable:
                    session.commit()
                else:
                    session.rollback()

    @classmethod
    def rename_if_not_exists(cls, element):
        """Rename an empty string to "-". The string is not
        modified if it is not empty.

        Args:
            element (string): element to rename.

        Returns:
            string: the modified (or unmodified) element
        """
        if not element:
            return "-"
        return element

    @classmethod
    def add_favorite(cls, original_prod, substitute_prod):
        """Adds to the list of favorites the pair of product to be replaced and substitute product

        Args:
            original_prod (object): Product to be replaced
            substitute_prod (object): Substitute product
        """
        substitute_prod.all_originals.append(original_prod)
        session.add(substitute_prod)
        session.commit()

    @classmethod
    def get_favorites_of(cls, original_prod):
        """Returns the favorite substitutes for a given product.

        Args:
            original_prod (object): Product for which we want to find
            the preferred substitutes.

        Returns:
            list of strings: Name of each favorite substitute product
        """
        return original_prod.all_substitutes

    @classmethod
    def get_categories_from_products(cls, products):
        """Returns the name of the categories of each product for a given
        list of products.

        Args:
            products (list of objects): Products we want to find there
            categories.

        Returns:
            list of strings: Name of each category
        """
        categories = set()
        for product in products:
            categories_list = product.list_of_categories
            for category in categories_list:
                categories.add(category.category_name)
        return categories

    @classmethod
    def get_products_from_subcategory(cls, main_category, subcategory):
        """Returns the products that are in common between the main category
        and the subcategory.

        Args:
            main_category (string): Name of the main category (Beverages
            or Food)
            subcategory (string): Name of subcategory

        Returns:
            list of objects: products
        """
        subcategory_prods = main_category_prods = []
        category_obj = (
            session.query(Category)
            .filter(Category.category_name == subcategory)
            .one_or_none())

        if category_obj:
            subcategory_prods = category_obj.list_of_products

        main_category_obj = (session.query(Category)
                             .filter(Category
                                     .category_name == main_category)
                             .one_or_none())
        if main_category_obj:
            main_category_prods = main_category_obj.list_of_products

        return {
            prod for prod in subcategory_prods if prod in main_category_prods}

    @classmethod
    def get_better_prods(cls, product):
        """Get a list of products similar to the one entered as an argument. From
        the most similar to the least similar and then by order of quality.
        To do this, we get the products that have the same categories in
        common.The number of categories in common is the weight of a product.
        The products are therefore classified from the most important weight to
        the least important then by nutriscore_grade.

        Args:
            product (object): Product for which we want to obtain a similar one

        Returns:
            List of tuples: List of pairs. One pair is (product, weight).
        """

        cats_of_the_chosen_product = product.list_of_categories
        categories_names = [
            category.category_name for category in cats_of_the_chosen_product]

        # One pair (product, weight) = product + list of categories in
        # common with the << selected product >>
        list_of_pairs = (
            session.query(
                Product, func.count(Product.id).label('category_count')
            )
            .join(Product.list_of_categories)
            .filter(Category.category_name.in_(categories_names),
                    Product.id != product.id,
                    Product.nutriscore < product.nutriscore)
            .group_by(Product)
            .order_by(desc('category_count'),
                      Product.nutriscore,
                      Product.product_name)
            .limit(MAX_PRODS_DISPLAYED)
            .all())

        return list_of_pairs

    @classmethod
    def get_favorites(cls):
        """Get the list of substitutes for each product then return a list of
        pairs (product, list of substitutes).

        Returns:
            List of pairs: A pair is constituted as follows:
            (product, list of substitutes)
        """
        try:
            products = session.query(Product).all()
            pairs__original_vs_substitute = []
            for product in products:
                substitute_prods = product.all_substitutes
                if len(substitute_prods) > 0:
                    pairs__original_vs_substitute.append(
                        (product, substitute_prods))

            return pairs__original_vs_substitute

        except Exception as e:
            print(str(e))

    @classmethod
    def delete_fav_substitute(cls, original, substitute):
        """Delete a product from a list of substitutes

        Args:
            original (object): The original product for which we want to remove
            a substitute.
            substitute (object): The substitute we want to remove from the list
        """
        try:
            products = (
                session.query(Product)
                .filter(Product.product_name == original.product_name)
                .all())

            for product in products:
                if substitute in product.all_substitutes:
                    product.all_substitutes.remove(substitute)
            session.commit()
        except Exception as e:
            e_traceback = traceback.format_exc()
            logger.error(f"""
            {ERROR_COLOR}
            ******************************************
            {e_traceback}
            ******************************************
            {str(e)}""")
            sys.exit(ic())

    @classmethod
    def only_food_list(cls):
        """Return a list of products that are not beverages

        Returns:
            list of objects: products that are not beverages
        """
        return (
            session.query(Product)
            .filter(Product.main_group != EN_BEVERAGES)
            .all())
