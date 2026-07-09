from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.database import SessionLocal


from app.schemas.stock import (
    StockCreate,
    StockUpdate,
    StockResponse
)


from app.crud.stock import (
    create_stock,
    update_stock,
    get_stock
)



router = APIRouter(
    prefix="/stocks",
    tags=["Stock"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()




@router.post(
    "",
    response_model=StockResponse
)
def create(
    stock: StockCreate,
    db: Session = Depends(get_db)
):

    return create_stock(
        db,
        stock
    )


@router.put(
    "/{product_id}",
    response_model=StockResponse
)
def update(
    product_id:int,
    stock:StockUpdate,
    db:Session=Depends(get_db)
):

    return update_stock(
        db,
        product_id,
        stock
    )




@router.get(
    "/{product_id}",
    response_model=StockResponse
)
def read(
    product_id:int,
    db:Session=Depends(get_db)
):

    return get_stock(
        db,
        product_id
    )