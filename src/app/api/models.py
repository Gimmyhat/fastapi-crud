from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)

    submenus = relationship('Submenu', cascade='all, delete')
    dishes = relationship('Dish', cascade='all, delete')

    @property
    def submenus_count(self):
        return len(self.submenus)

    @property
    def dishes_count(self):
        return len(self.dishes)


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)

    menu_id = Column(Integer, ForeignKey('menus.id'))
    dishes = relationship('Dish', cascade='all, delete')

    @property
    def dishes_count(self):
        return len(self.dishes)


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    price = Column(Numeric(precision=10, scale=2))

    menu_id = Column(Integer, ForeignKey('menus.id'))
    submenu_id = Column(Integer, ForeignKey('submenus.id'))
