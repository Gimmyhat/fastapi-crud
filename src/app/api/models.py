from typing import List, Union

from app.db import Base
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# SQLAlchemy Model


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)

    menu_id = Column(Integer, ForeignKey('menus.id'))
    menu = relationship('Menu', backref='submenus')


# Pydantic Model

class SubmenuBase(BaseModel):
    title: str
    description: Union[str, None] = None


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: int
    menu_id: int

    class Config:
        orm_mode = True


class MenuSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    dishes_count: int = 0


class MenuDB(MenuSchema):
    id: int
    submenus: List[Submenu] = []

    class Config:
        orm_mode = True
