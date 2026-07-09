from sqlalchemy.orm import Session

from app.models.store import Store
from app.schemas.store import StoreCreate



def create_store(
    db: Session,
    store: StoreCreate
):

    db_store = Store(
        name=store.name,
        location=store.location
    )


    db.add(db_store)

    db.commit()

    db.refresh(db_store)


    return db_store



def get_stores(
    db: Session
):

    return db.query(Store).all()