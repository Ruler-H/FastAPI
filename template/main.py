from typing import Optional
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(docs_url="/documentation", redoc_url=None)

templates = Jinja2Templates(directory="templates")


# @app.get("/")
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/about", response_class=HTMLResponse)
# def about():
#     return "<h1>Hello World 2</h1>"


# @app.get("/contact", response_class=HTMLResponse)
# def contact():
#     return "<h1>Hello World 3</h1>"


# @app.get("/notice", response_class=HTMLResponse)
# def notice():
#     return "<h1>Hello World 4</h1>"


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(user_id: int, item_id: str):
#     return {"user_id": user_id, "item_id": item_id}


# @app.get("/hello/{name}", response_class=HTMLResponse)
# async def hello(name: str):
#     return "<h1>Hello, " + name + "</h1>"


# @app.get("/calculate/{operation}/{a}/{b}")
# async def calculate(operation: str, a: int, b: int):
#     if operation == "add":
#         return {"result": a + b}
#     elif operation == "subtract":
#         return {"result": a - b}
#     elif operation == "multiply":
#         return {"result": a * b}
#     elif operation == "divide":
#         return {"result": a / b}
#     else:
#         return {"error": "Operation not supported."}


# class Item(BaseModel):
#     name: str
#     price: float


# @app.post("/items")
# async def create_item(item: Item):
#     return {"item": item}


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, "item": item}


# class ItemDetail(BaseModel):
#     description: str
#     weight: float


# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     taxs: float = 10.5


# @app.post("/items")
# async def create_item(item: Item):
#     return {"item": item}


# class User(BaseModel):
#     name: str
#     email: str
#     age: int


# @app.post("/user")
# async def create_user(user: User):
#     return {"user": user}


# class Post(BaseModel):
#     title: str
#     content: str
#     author: User


# @app.post("/post")
# async def create_post(post: Post):
#     return {"post": post}


# class Item(BaseModel):
#     item_id: int = Field(..., ge=1, le=10)
#     price: float = Field(..., gt=0)


# @app.get("/items")
# async def read_items(
#     # item_id: int = Query(..., ge=1, le=10), price: float = Query(..., gt=0)
#     item_id: int,
#     price: float,
# ):
#     item = Item(item_id=item_id, price=price)
#     return {"item": item}


# @app.get("/items")
# async def read_items(item_id: int, is_available: bool = True):
#     return {"item_id": item_id, "is_available": is_available}


products = [
    {
        "name": "Mobile",
        "price": 1000,
        "available": True,
    },
    {
        "name": "Laptop",
        "price": 2000,
        "available": False,
    },
    {
        "name": "Tablet",
        "price": 500,
        "available": True,
    },
]


@app.get("/product")
async def find_product(
    name: str = Query(None, min_length=3, max_length=50),
    min_price: float = Query(None, gt=0, le=1000),
    max_price: float = Query(None, gt=0, le=1000),
    available: bool = Query(None),
):
    print("name:", name)
    print("min_price:", min_price)
    print("max_price:", max_price)
    print("available:", available)
    find_products = products.copy()
    if name:
        find_products = list(
            filter(lambda p: name.lower() in p["name"].lower(), find_products)
        )
    if min_price:
        find_products = list(filter(lambda p: p["price"] >= min_price, find_products))
    if max_price:
        find_products = list(filter(lambda p: p["price"] <= max_price, find_products))
    if available is not None:
        find_products = list(
            filter(lambda p: p["available"] == available, find_products)
        )
    return {"products": find_products}


class User(BaseModel):
    name: str
    email: str
    age: int


@app.get("/user")
async def read_user(page: int = 1, size: int = 10, sort_by: str = "name"):
    """
    사용자 목록 조회
    페이지네이션 처리
    """

    return {"page": page, "size": size, "sort_by": sort_by}
