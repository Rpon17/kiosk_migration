from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.database import SessionLocal


from app.schemas.product import (
    ProductCreate,
    ProductResponse
)


from app.crud.product import (
    create_product,
    get_products
)



router = APIRouter(
    prefix="/products",
    tags=["Product"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()




@router.post(
    "",
    response_model=ProductResponse
)
def create(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    return create_product(
        db,
        product
    )



@router.get(
    "/category/{category_id}",
    response_model=list[ProductResponse]
)
def read_by_category(
    category_id:int,
    db: Session = Depends(get_db)
):

    return get_products(
        db,
        category_id
    )