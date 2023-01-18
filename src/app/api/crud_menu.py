from app.api.models import *
from sqlalchemy.orm import Session

table = Menu


def post(db_session: Session, payload: BaseSchema):
    menu = table(title=payload.title, description=payload.description)
    db_session.add(menu)
    db_session.commit()
    db_session.refresh(menu)
    return menu


def get(db_session: Session, id: int):
    return db_session.query(table).filter(table.id == id).first()


def get_all(db_session: Session):
    return db_session.query(table).all()


def put(db_session: Session, menu: table, title: str, description: str):
    menu.title = title
    menu.description = description
    db_session.commit()
    return menu


def delete(db_session: Session, id: int):
    menu = db_session.query(table).filter(table.id == id).first()
    db_session.delete(menu)
    db_session.commit()
    return menu
