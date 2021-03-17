import os

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from constants import (
    BRAND_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    INGREDIENTS_MAX_LENGTH,
    PRODUCT_NAME_MAX_LENGTH,
    SHOP_NAME_MAX_LENGTH,
    )


load_dotenv()
DATABASE = os.getenv("DATABASE")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")

Base = declarative_base()

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}"
    # f"mysql+mysqlconnector://root:8571Prestij@localhost/OCP5"
)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

l_category_and_product = Table(
    'l_category_product',
    Base.metadata,
    Column('fk_product_id', Integer, ForeignKey('product.id')),
    Column('fk_category_id', Integer, ForeignKey('category.category_id')))


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(PRODUCT_NAME_MAX_LENGTH), nullable=False)
    nutriscore = Column(String(2), nullable=False)
    ingredients = Column(String(INGREDIENTS_MAX_LENGTH), nullable=False)
    # brand = Column(String(BRAND_NAME_MAX_LENGTH), nullable=False)
    list_of_categories = relationship(
        "Category",
        secondary=l_category_and_product,
        back_populates="list_of_products",
        cascade="all, delete",
        passive_deletes=True)

    @classmethod
    def fill_database(cls, products, categories, stores):
        for product in products:
            is_commitable = False
            new_product = Product(
                product_name=product.get('product_name'),
                nutriscore=product.get("nutriscore_grade"),
                ingredients=product.get("ingredients"))
            session.add(new_product)

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


class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(CATEGORY_NAME_MAX_LENGTH), nullable=False)
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


# class Shop(Base):
#     __tablename__ = 'shop'
#     shop_id = Column(Integer, primary_key=True)
#     shop_name = Column(String(SHOP_NAME_MAX_LENGTH), nullable=False)

#     @classmethod
#     def fill_database(cls, stores):
#         for store in stores:
#             if store:
#                 new_store = Shop(shop_name=store)
#                 session.add(new_store)
#                 session.flush()  # To get the inserted id
#                 session.commit()
#         print("Voici le last insert id: ", new_store.shop_id)


# class Favorite(Base):
#     __tablename__ = 'favorite'
#     fav_id = Column(Integer, primary_key=True)
#     fk_bad_product_id = Column(Integer, ForeignKey('product.id'))
#     fk_good_product_id = Column(Integer, ForeignKey('shop.shop_id'))
#     product = relationship(Product)
#     shop = relationship(Shop)
