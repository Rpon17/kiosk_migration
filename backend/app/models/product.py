from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(String(100), nullable=False)

    price = Column(Integer, nullable=False)

    image_url = Column(String(500))

    category = relationship(
        "Category", 
        back_populates="products"
        )

    stock = relationship(
        "Stock",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan"
    )