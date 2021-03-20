import os
import sys

from unidecode import unidecode
from icecream import ic

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, exc
from sqlalchemy import create_engine

from constants import (
    BRAND_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
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

    # List of products that belong to a category
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


# class Favorite(Base):
#     __tablename__ = 'favorite'
#     fav_id = Column(Integer, primary_key=True)
#     fk_bad_product_id = Column(Integer, ForeignKey('product.id'))
#     fk_good_product_id = Column(Integer, ForeignKey('store.store_id'))
#     product = relationship(Product)
#     store = relationship(Shop)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(PRODUCT_NAME_MAX_LENGTH), nullable=False)
    nutriscore = Column(String(2), nullable=False)
    ingredients = Column(String(INGREDIENTS_MAX_LENGTH), nullable=False)

    # brand = Column(String(BRAND_NAME_MAX_LENGTH), nullable=False)

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
