from fastapi import FastAPI


from app.routers import (
    store,
    category,
    product,
    stock
)



app = FastAPI()



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