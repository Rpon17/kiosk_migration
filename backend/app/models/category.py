from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)

    name = Column(String(100), nullable=False)

    store = relationship(
        "Store", 
        back_populates="categories"
        )
    
    
    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )