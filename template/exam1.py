from typing import Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    user_id: int
    username: str
    email: str
    password: Optional[str] = None


@app.get("/users/{user_id}", response_model=User, response_model_exclude={"password"})
async def read_user(user_id: int):
    return {
        "user_id": user_id,
        "username": "johndoe",
        "email": "elwl5515@gmail.com",
        "password": "secret",
    }


class Product(BaseModel):
    product_id: int
    name: str
    price: float
    stock: Optional[int] = None


class Message(BaseModel):
    message: str


@app.get(
    "/products/{mode}/{product_id}",
    response_model=Union[Product, Message],
)
async def read_product(mode: str, product_id: int):
    if mode == "basic":
        return {"product_id": product_id, "name": "sample product", "price": 999.99}
    elif mode == "detail":
        return {
            "product_id": product_id,
            "name": "sample product",
            "price": 999.99,
            "stock": 100,
        }
    else:
        return {"message": "Mode not supported."}
