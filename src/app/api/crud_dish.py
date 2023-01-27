from .models import *
from sqlalchemy.orm import Session

table = Dish


def post(db_session: Session, payload: DishDB, menu_id: int, submenu_id: int):
    dish = table(title=payload.title, description=payload.description,
                 price=payload.price, menu_id=menu_id, submenu_id=submenu_id)
    db_session.add(dish)
    db_session.commit()
    db_session.refresh(dish)
    return dish


def get(db_session: Session, id: int, submenu_id: int):
    return db_session.query(table) \
        .filter(table.id == id and table.submenu_id == submenu_id).first()


def get_all(db_session: Session, submenu_id: int):
    return db_session.query(table).filter(table.submenu_id == submenu_id).all()


def put(db_session: Session, dish: table, title: str, description: str, price: str):
    dish.title = title
    dish.description = description
    dish.price = price
    db_session.commit()
    return dish


def delete(db_session: Session, dish: table):
    db_session.delete(dish)
    db_session.commit()
    return dish
