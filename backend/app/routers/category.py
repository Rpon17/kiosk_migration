from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.schemas.category import (
    CategoryCreate,
    CategoryResponse
)

from app.crud.category import (
    create_category,
    get_categories
)



router = APIRouter(
    prefix="/categories",
    tags=["Category"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post(
    "",
    response_model=CategoryResponse
)
def create(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    return create_category(
        db,
        category
    )



@router.get(
    "/store/{store_id}",
    response_model=list[CategoryResponse]
)
def read_by_store(
    store_id: int,
    db: Session = Depends(get_db)
):

    return get_categories(
        db,
        store_id
    )