from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    store,
    category,
    product,
    stock
)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ], 
    allow_credentials=True,
    allow_methods=["*"],  # OPTIONS, GET, POST 등 모든 메서드 허용
    allow_headers=["*"],  # Content-Type 등 모든 헤더 허용
)


app.include_router(
    store.router
)


app.include_router(
    category.router
)


app.include_router(
    product.router
)


app.include_router(
    stock.router
)



@app.get("/")
def root():

    return {
        "message":"POS API Server"
    }