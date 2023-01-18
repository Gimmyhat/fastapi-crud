from fastapi import FastAPI

from app.db import engine
from app.api import ping, routes
from app.api.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routes.router, prefix="/api/v1/menus", tags=["menus"])
