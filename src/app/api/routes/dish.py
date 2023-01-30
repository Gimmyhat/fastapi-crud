from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from ..crud import Session, create_model, get_models, update_model, delete_model, get_model
from ..models import Dish
from ..schemas import DishDB, BaseSchema, DishSchema
from ...db import get_db

router = APIRouter()


@router.post("/{menu_id}/submenus/{submenu_id}/dishes/", response_model=DishDB, status_code=201)
def create_dish(*, db: Session = Depends(get_db),
                payload: DishSchema,
                menu_id: int = Path(..., gt=0),
                submenu_id: int = Path(..., gt=0)):
    payload = dict(payload)
    payload['menu_id'] = menu_id
    payload['submenu_id'] = submenu_id
    dish = create_model(db=db, model=Dish, schema=payload)
    return dish


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/", response_model=DishDB, status_code=200)
def read_dish(*, db: Session = Depends(get_db),
              dish_id: int = Path(..., gt=0)):
    dish = get_model(db=db, model=Dish, model_id=dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/", response_model=List[DishDB])
def read_all_dishes(db: Session = Depends(get_db),
                    menu_id: int = Path(..., gt=0),
                    submenu_id: int = Path(..., gt=0)):
    return get_models(db=db, model=Dish)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/",
              response_model=DishDB, status_code=200)
def update_dish(*, db: Session = Depends(get_db),
                dish_id: int = Path(..., gt=0),
                payload: DishSchema):
    dish = get_model(db=db, model=Dish, model_id=dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    dish = update_model(db=db, model=Dish, model_id=dish_id, schema=dict(payload))
    return dish


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/", response_model=DishDB, status_code=200)
def delete_dish(*, db: Session = Depends(get_db), dish_id: int = Path(..., gt=0)):
    dish = get_model(db=db, model=Dish, model_id=dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    delete_model(db=db, model=Dish, model_id=dish_id)
    return dish
