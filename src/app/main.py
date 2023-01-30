from fastapi import FastAPI

from .api.models import Base
from .api.routes import menu, submenu, dish
from .db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
prefix = '/api/v1/menus'
prefix_submenu = '/api/v1/menus/{menu_id}/submenus'
prefix_dish = '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'


app.include_router(menu.router, prefix=prefix, tags=["menus"])
app.include_router(submenu.router, prefix=prefix, tags=["submenus"])
app.include_router(dish.router, prefix=prefix, tags=["dishes"])
