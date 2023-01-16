from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path

from app.db import SessionLocal
from app.api import crud
from app.api.models import MenuDB, MenuSchema


router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=MenuDB, status_code=201)
def create_menu(*, db: Session = Depends(get_db), payload: MenuSchema):
    menu = crud.post(db_session=db, payload=payload)
    return menu


@router.get("/{id}/", response_model=MenuDB)
def read_menu(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    menu = crud.get(db_session=db, id=id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.get("/", response_model=List[MenuDB])
def read_all_menus(db: Session = Depends(get_db)):
    return crud.get_all(db_session=db)


@router.put("/{id}/", response_model=MenuDB)
def update_menu(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0), payload: MenuSchema
):
    menu = crud.get(db_session=db, id=id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu = crud.put(
        db_session=db, menu=menu, title=payload.title, description=payload.description
    )
    return menu


@router.delete("/{id}/", response_model=MenuDB)
def delete_menu(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    menu = crud.get(db_session=db, id=id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu = crud.delete(db_session=db, id=id)
    return menu
