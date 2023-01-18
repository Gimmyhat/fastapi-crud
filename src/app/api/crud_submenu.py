from app.api.models import *
from sqlalchemy.orm import Session

table = Submenu


def post(db_session: Session, payload: SubmenuDB, menu_id: int):
    submenu = table(title=payload.title, description=payload.description, menu_id=menu_id)
    db_session.add(submenu)
    db_session.commit()
    db_session.refresh(submenu)
    return submenu


def get(db_session: Session, id: int, menu_id: int):
    return db_session.query(table).filter(table.id == id and table.menu_id == menu_id).first()


def get_all(db_session: Session, menu_id: int):
    return db_session.query(table).filter(table.menu_id == menu_id).all()


def put(db_session: Session, submenu: table, title: str, description: str):
    submenu.title = title
    submenu.description = description
    db_session.commit()
    return submenu


def delete(db_session: Session, submenu: table):
    db_session.delete(submenu)
    db_session.commit()
    return submenu
