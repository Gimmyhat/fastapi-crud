from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db import Base


# SQLAlchemy Model


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)

    submenus = relationship('Submenu', cascade='all, delete')
    dishes = relationship('Dish', cascade='all, delete')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)

    menu_id = Column(Integer, ForeignKey('menus.id'))
    dishes = relationship('Dish', cascade='all, delete')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    price = Column(Numeric(precision=10, scale=2))

    menu_id = Column(Integer, ForeignKey('menus.id'))
    submenu_id = Column(Integer, ForeignKey('submenus.id'))


# Pydantic Model


class BaseSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True


class DishSchema(BaseSchema):
    price: str


class DishDB(DishSchema):
    id: str


class SubmenuDB(BaseSchema):
    id: str
    dishes_count: int = 0


class MenuDB(BaseSchema):
    id: str
    submenus_count: int = 0
    dishes_count: int = 0
