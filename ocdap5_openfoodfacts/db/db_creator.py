import os
import sys
from sqlalchemy.sql import elements

from unidecode import unidecode
from icecream import ic
from pprint import pprint

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    desc,
    ForeignKey,
    func,
    Integer,
    String,
    Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.expression import true, and_

from constants import (
    BEVERAGES,
    BRAND_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    INGREDIENTS_MAX_LENGTH,
    LIST_OF_BEVERAGES_THAT_ARE_FOOD_TOO,
    MAX_PRODS_DISPLAYED,
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

    def __str__(self):
        return self.brand_name.title()

    def __repr__(self):
        return self.brand_name.title()

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
        passive_deletes=True,
        lazy='joined')

    def __str__(self):
        return self.category_name.title()
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

    @classmethod
    def set_beverages_that_are_food_too(self):
        for dual_cat in LIST_OF_BEVERAGES_THAT_ARE_FOOD_TOO:
            beverages_that_are_food = (
                session.query(Category)
                .filter(Category.category_name.like(f"{dual_cat}%"))
                .all())
            for category in beverages_that_are_food:
                category.is_beverage = True
                category.is_food = True
            session.commit()


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

    def __str__(self):
        return self.store_name.title()

    def __repr__(self):
        return self.store_name.title()

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

    def __str__(self):
        return self.product_name.title()

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
        session.add(substitute_prod)
        session.commit()

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

    @classmethod
    def get_products_from_subcategory(cls, main_category, subcategory):
        subcategory_prods = main_category_prods = []
        category_obj = (
            session.query(Category)
            .filter(Category.category_name == subcategory)
            .one_or_none())
        if category_obj:
            subcategory_prods = category_obj.list_of_products

        beverages_cat = (session.query(Category)
                         .filter(Category
                                 .category_name == main_category)
                         .one_or_none())
        if beverages_cat:
            main_category_prods = beverages_cat.list_of_products

        return {
            prod for prod in subcategory_prods if prod in main_category_prods}

    @classmethod
    def get_better_prods(self, product):

        cats_of_the_chosen_product = product.list_of_categories
        categories_names = [
            category.category_name for category in cats_of_the_chosen_product]
        # One pair (product, weight) = product + list of categories in
        # common with the selected product
        list_of_pairs = (
            session.query(
                Product, func.count(Product.id).label('category_count')
            )
            .join(Product.list_of_categories)
            .filter(Category.category_name.in_(categories_names))
            .group_by(Product)
            .order_by(desc('category_count'),
                      Product.nutriscore,
                      Product.product_name)
            .limit(MAX_PRODS_DISPLAYED)
            .all())

        return list_of_pairs
