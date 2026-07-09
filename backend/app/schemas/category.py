from pydantic import BaseModel


class CategoryCreate(BaseModel):

    store_id: int
    name: str



class CategoryResponse(BaseModel):

    id: int
    store_id: int
    name: str


    class Config:
        from_attributes = True