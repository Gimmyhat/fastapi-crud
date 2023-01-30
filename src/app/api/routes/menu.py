from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from ..crud import Session, create_model, get_model, get_models, update_model, delete_model
from ..models import Menu
from ..schemas import MenuDB, BaseSchema
from ...db import get_db

router = APIRouter()


@router.post("/", response_model=MenuDB, status_code=201)
def create_menu(*, db: Session = Depends(get_db), payload: BaseSchema):
    menu = create_model(db=db, model=Menu, schema=dict(payload))
    return menu


@router.get("/{menu_id}/", response_model=MenuDB, status_code=200)
def read_menu(*, db: Session = Depends(get_db), menu_id: int = Path(..., gt=0)):
    menu = get_model(db=db, model=Menu, model_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.get("/", response_model=List[MenuDB], status_code=200)
def read_all_menus(db: Session = Depends(get_db)):
    return get_models(db=db, model=Menu)


@router.patch("/{menu_id}/", response_model=BaseSchema, status_code=200)
def update_menu(
        *, db: Session = Depends(get_db), menu_id: int = Path(..., gt=0), payload: BaseSchema):
    menu = get_model(db=db, model=Menu, model_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu = update_model(db=db, model=Menu, model_id=menu_id, schema=dict(payload))
    return menu


@router.delete("/{menu_id}/", response_model=MenuDB, status_code=200)
def delete_menu(*, db: Session = Depends(get_db), menu_id: int = Path(..., gt=0)):
    menu = get_model(db=db, model=Menu, model_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    delete_model(db=db, model=Menu, model_id=menu_id)
    return menu
