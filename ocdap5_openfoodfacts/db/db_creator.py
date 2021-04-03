import os
import sys

from unidecode import unidecode
from icecream import ic
from pprint import pprint

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    ForeignKey,
    Integer,
    String,
    Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.expression import false, true

from constants import (
    BEVERAGES,
    BRAND_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    FOOD,
    INGREDIENTS_MAX_LENGTH,
    NUTRISCORE_MAX_LENGTH,
    PRODUCT_NAME_MAX_LENGTH,
    STORE_NAME_MAX_LENGTH)

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

    @classmethod
    def fill_database(cls, brands):
        for brand in brands:
            new_brand = Brand(brand_name=str(brand))
            session.add(new_brand)
            session.commit()


class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(CATEGORY_NAME_MAX_LENGTH),
                           nullable=False,
                           unique=True)
    is_beverage = Column(Boolean, default=False)
    is_food = Column(Boolean, default=True)

    # List of products that belong to a selected category
    list_of_products = relationship(
        "Product",
        secondary=l_category_and_product,
        back_populates="list_of_categories",
        cascade="all, delete",
        passive_deletes=True)

    @classmethod
    def fill_database(cls, categories):
        for category in categories:
            new_category = Category(category_name=category)
            session.add(new_category)
            session.commit()

    @classmethod
    def extract_beverage_subcategories(cls, controller):
        """Collect a list of subcategories that are part of
        the main category: Beverage.

        Here is the process:
        1. Select the " Beverage" category
        2. Select all products in this category
        3. For each of the selected products, select all the associated
            categories as they are necessarily part of "Beverages"
            and put them in beverage_categories_names.
        4. For each category from beverage_categories_names update
            its "is_beverage" field to true and its "is_food" field to false
        5. Add these categories to the "Beverages" list of the controller.
        """
        beverage = (session.query(Category)
                    .filter(Category.category_name == BEVERAGES)
                    .one())
        if beverage:
            # Collecting products from the Beverage category.
            products_list = beverage.list_of_products
            beverage_categories_names = Product.get_categories_from_product(
                products_list)
            for beverage_category_name in beverage_categories_names:
                category = (
                    session.query(Category)
                    .filter(Category.category_name == beverage_category_name)
                    .one())
                category.is_beverage = True
                category.is_food = False

            session.commit()
        else:
            print()
            print("**** No beverage found ! *****")
            print()

    @classmethod
    def get_beverages_list(cls):
        beverages = (
            session.query(Category.category_name)
            .filter(Category.is_beverage == true())
            .all())
        beverages = [str(elt).strip("()',\"") for elt in beverages]
        beverages.sort()
        return beverages

    @classmethod
    def get_food_list(cls):
        food_list = (
            session.query(Category.category_name)
            .filter(Category.is_food == true())
            .all())
        food_list = [str(elt).strip("()',\"") for elt in food_list]
        food_list.sort()
        return food_list


class Store(Base):
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

    @classmethod
    def fill_database(cls, stores):
        for store in stores:
            new_store = Store(store_name=store)
            session.add(new_store)
            session.commit()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(PRODUCT_NAME_MAX_LENGTH), nullable=False)
    nutriscore = Column(String(2), nullable=False)
    ingredients = Column(String(INGREDIENTS_MAX_LENGTH), nullable=False)

    # List of categories to which a product belongs
    list_of_categories = relationship(
        "Category",
        secondary=l_category_and_product,
        back_populates="list_of_products",
        cascade="all, delete",
        passive_deletes=True)

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

    # list of original products for one substitute product
    all_substitutes = relationship(
        'Product',
        secondary=l_original_and_substitute,
        primaryjoin=id == l_original_and_substitute.c
        .original_prod_id,
        secondaryjoin=id == l_original_and_substitute.c
        .substitute_prod_id,
        backref='all_originals'
    )

    @classmethod
    def fill_database(cls, products, brands, categories, stores):
        for product in products:

            ingredients_str = product.get("ingredients")
            ingredients_str = cls.rename_if_not_exists(ingredients_str)

            nutriscore_str = product.get("nutriscore_grade")
            nutriscore_str = cls.rename_if_not_exists(nutriscore_str)

            product_name_str = product.get("product_name")
            product_name_str = cls.rename_if_not_exists(product_name_str)

            is_commitable = False

            # insert product
            new_product = Product(
                product_name=product_name_str,
                nutriscore=nutriscore_str,
                ingredients=ingredients_str)
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
        if not element:
            return "-"
        return element

    @classmethod
    def add_favorite(cls, original_prod, substitute_prod):
        substitute_prod.all_originals.append(original_prod)

    @classmethod
    def get_favorites_of(cls, original_prod):
        return original_prod.all_substitutes

    @classmethod
    def get_categories_from_product(cls, products):
        categories = set()
        for product in products:
            categories_list = product.list_of_categories
            for category in categories_list:
                categories.add(category.category_name)
        return categories
