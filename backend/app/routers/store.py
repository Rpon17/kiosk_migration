from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.schemas.store import (
    StoreCreate,
    StoreResponse
)

from app.crud.store import (
    create_store,
    get_stores
)


router = APIRouter(
    prefix="/stores",
    tags=["Store"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post(
    "",
    response_model=StoreResponse
)
def create(
    store: StoreCreate,
    db: Session = Depends(get_db)
):

    return create_store(
        db,
        store
    )



@router.get(
    "",
    response_model=list[StoreResponse]
)
def read_all(
    db: Session = Depends(get_db)
):

    return get_stores(db)