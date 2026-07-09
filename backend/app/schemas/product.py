from pydantic import BaseModel


class ProductCreate(BaseModel):

    category_id: int
    name: str
    price: int
    image_url: str | None = None



class ProductResponse(BaseModel):

    id: int
    category_id: int
    name: str
    price: int
    image_url: str | None


    class Config:
        from_attributes = True