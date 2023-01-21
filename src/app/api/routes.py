from app.api import crud_menu, crud_submenu, crud_dish
from app.api.models import *
from app.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

router = APIRouter()

menu_schema = MenuDB
submenu_schema = SubmenuDB
dish_schema = DishDB
base_schema = BaseSchema


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=menu_schema, status_code=201)
def create_menu(*, db: Session = Depends(get_db), payload: base_schema):
    menu = crud_menu.post(db_session=db, payload=payload)
    return menu


@router.get("/{id}/", response_model=menu_schema)
def read_menu(
        *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    menu = crud_menu.get(db_session=db, id=id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    if isinstance(menu, dict):
        return menu
    return {"title": menu.title,
            "description": menu.description,
            "id": menu.id,
            "submenus_count": len(menu.submenus),
            "dishes_count": len(menu.dishes)}


@router.get("/", response_model=List[menu_schema])
def read_all_menus(db: Session = Depends(get_db)):
    return crud_menu.get_all(db_session=db)


@router.patch("/{id}/", response_model=base_schema, status_code=200)
def update_menu(
        *, db: Session = Depends(get_db), id: int = Path(..., gt=0), payload: base_schema
):
    menu = crud_menu.get(db_session=db, id=id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu = crud_menu.put(
        db_session=db, menu=menu, title=payload.title, description=payload.description
    )
    return menu


@router.delete("/{id}/", response_model=menu_schema, status_code=200)
def delete_menu(
        *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    menu = crud_menu.get(db_session=db, id=id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu = crud_menu.delete(db_session=db, id=id)
    return menu


# Submenu

@router.post("/{menu_id}/submenus", response_model=submenu_schema, status_code=201)
def create_submenu(*, db: Session = Depends(get_db),
                   payload: base_schema, menu_id: int = Path(..., gt=0)):
    submenu = crud_submenu.post(db_session=db, payload=payload, menu_id=menu_id)
    return submenu


@router.get("/{menu_id}/submenus", response_model=List[submenu_schema])
def read_all_submenus(db: Session = Depends(get_db), menu_id: int = Path(..., gt=0)):
    return crud_submenu.get_all(db_session=db, menu_id=menu_id)


@router.get("/{menu_id}/submenus/{id}/", response_model=submenu_schema, status_code=200)
def read_submenu(
        *, db: Session = Depends(get_db), menu_id: int = Path(..., gt=0), id: int = Path(..., gt=0)
):
    submenu = crud_submenu.get(db_session=db, menu_id=menu_id, id=id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    dishes_count = db.query(Submenu.dishes).filter(Submenu.id == id).count()
    if isinstance(submenu, dict):
        return submenu
    return {"title": submenu.title,
            "description": submenu.description,
            "id": submenu.id,
            "dishes_count": dishes_count}


@router.patch("/{menu_id}/submenus/{id}/", response_model=submenu_schema, status_code=200)
def update_submenu(
        *, db: Session = Depends(get_db), menu_id: int = Path(..., gt=0),
        id: int = Path(..., gt=0), payload: base_schema
):
    submenu = crud_submenu.get(db_session=db, menu_id=menu_id, id=id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu = crud_submenu.put(
        db_session=db, submenu=submenu, title=payload.title, description=payload.description
    )
    return submenu


@router.delete("/{menu_id}/submenus/{id}/", response_model=submenu_schema, status_code=200)
def delete_submenu(
        *, db: Session = Depends(get_db), menu_id: int = Path(..., gt=0),
        id: int = Path(..., gt=0)
):
    submenu = crud_submenu.get(db_session=db, menu_id=menu_id, id=id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu = crud_submenu.delete(db_session=db, submenu=submenu)
    return submenu


# Dish

@router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=dish_schema, status_code=201)
def create_dish(*, db: Session = Depends(get_db),
                payload: DishSchema, menu_id: int = Path(..., gt=0),
                submenu_id: int = Path(..., gt=0)):
    dish = crud_dish.post(db_session=db, payload=payload, menu_id=menu_id, submenu_id=submenu_id)
    return dish


@router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[dish_schema])
def read_all_dishes(db: Session = Depends(get_db), submenu_id: int = Path(..., gt=0)):
    return crud_dish.get_all(db_session=db, submenu_id=submenu_id)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{id}/", response_model=dish_schema, status_code=200)
def read_dish(
        *, db: Session = Depends(get_db), submenu_id: int = Path(..., gt=0), id: int = Path(..., gt=0)
):
    dish = crud_dish.get(db_session=db, submenu_id=submenu_id, id=id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{id}/", response_model=DishSchema, status_code=200)
def update_dish(
        *, db: Session = Depends(get_db), submenu_id: int = Path(..., gt=0),
        id: int = Path(..., gt=0), payload: DishSchema
):
    dish = crud_dish.get(db_session=db, submenu_id=submenu_id, id=id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    dish = crud_dish.put(
        db_session=db, dish=dish, title=payload.title, description=payload.description,
        price=payload.price
    )
    return dish


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{id}/", response_model=DishSchema, status_code=200)
def delete_dish(
        *, db: Session = Depends(get_db), submenu_id: int = Path(..., gt=0),
        id: int = Path(..., gt=0)
):
    dish = crud_dish.get(db_session=db, submenu_id=submenu_id, id=id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    dish = crud_dish.delete(db_session=db, dish=dish)
    return dish
