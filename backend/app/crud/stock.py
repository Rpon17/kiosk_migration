from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockUpdate



def create_stock(
    db: Session,
    stock: StockCreate
):

    db_stock = Stock(

        product_id=stock.product_id,

        quantity=stock.quantity
    )


    db.add(db_stock)

    db.commit()

    db.refresh(db_stock)


    return db_stock



def update_stock(
    db: Session,
    product_id: int,
    stock: StockUpdate
):

    db_stock = (
        db.query(Stock)
        .filter(
            Stock.product_id == product_id
        )
        .first()
    )


    if db_stock:

        db_stock.quantity = stock.quantity

        db.commit()

        db.refresh(db_stock)


    return db_stock



def get_stock(
    db: Session,
    product_id: int
):

    return (
        db.query(Stock)
        .filter(
            Stock.product_id == product_id
        )
        .first()
    )