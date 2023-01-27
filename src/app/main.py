from fastapi import FastAPI

from .db import engine
from .api import routes
from .api.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routes.router, prefix="/api/v1/menus", tags=["menus"])
