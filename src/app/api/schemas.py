from pydantic import BaseModel, Field


# Pydantic Model

class BaseSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True


class DishSchema(BaseSchema):
    price: str


class DishDB(DishSchema):
    id: str


class SubmenuDB(BaseSchema):
    id: str
    dishes_count: int = 0


class MenuDB(BaseSchema):
    id: str
    submenus_count: int = 0
    dishes_count: int = 0
