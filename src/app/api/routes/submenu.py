from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from ..crud import Session, create_model, get_models, update_model, delete_model, get_model
from ..models import Submenu
from ..schemas import SubmenuDB, BaseSchema
from ...db import get_db

router = APIRouter()


@router.post("/{menu_id}/submenus/", response_model=SubmenuDB, status_code=201)
def create_submenu(*, db: Session = Depends(get_db),
                   payload: BaseSchema, menu_id: int = Path(..., gt=0)):
    payload = dict(payload)
    payload['menu_id'] = menu_id
    submenu = create_model(db=db, model=Submenu, schema=payload)
    return submenu


@router.get("/{menu_id}/submenus/{submenu_id}/", response_model=SubmenuDB, status_code=200)
def read_submenu(*, db: Session = Depends(get_db),
                 submenu_id: int = Path(..., gt=0)):
    submenu = get_model(db=db, model=Submenu, model_id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@router.get("/{menu_id}/submenus/", response_model=List[SubmenuDB])
def read_all_submenus(db: Session = Depends(get_db),
                      menu_id: int = Path(..., gt=0)):
    return get_models(db=db, model=Submenu)


@router.patch("/{menu_id}/submenus/{submenu_id}/", response_model=BaseSchema, status_code=200)
def update_submenu(
        *, db: Session = Depends(get_db), submenu_id: int = Path(..., gt=0), payload: BaseSchema):
    submenu = get_model(db=db, model=Submenu, model_id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu = update_model(db=db, model=Submenu, model_id=submenu_id, schema=dict(payload))
    return submenu


@router.delete("/{menu_id}/submenus/{submenu_id}/", response_model=SubmenuDB, status_code=200)
def delete_submenu(*, db: Session = Depends(get_db), submenu_id: int = Path(..., gt=0)):
    submenu = get_model(db=db, model=Submenu, model_id=submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    delete_model(db=db, model=Submenu, model_id=submenu_id)
    return submenu
