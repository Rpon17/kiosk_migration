from datetime import datetime

from pydantic import BaseModel



class StockCreate(BaseModel):

    product_id: int
    quantity: int



class StockUpdate(BaseModel):

    quantity: int



class StockResponse(BaseModel):

    id: int
    product_id: int
    quantity: int
    updated_at: datetime


    class Config:
        from_attributes = True