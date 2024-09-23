from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DataBase setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DataBase Dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
)

items = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: str


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return item


@app.get("/items", response_model=List[Item], tags=["items"])
async def read_items():
    """
    Retrieve items.

    You can specify a category to filter the items.
    """
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    stored_item = items[item_id]
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)
    items[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items.pop(item_id)
    return item


@app.get("/items/search/{item_name}", response_model=List[Item])
async def read_item_by_name(item_name: str):
    findItemList = list(filter(lambda item: item_name in item.name, items.values()))
    if findItemList:
        return findItemList
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/category/{category}", response_model=List[Item])
async def read_item_by_category(category: str):
    findItemList = list(filter(lambda item: category in item.category, items.values()))
    if findItemList:
        return findItemList
    raise HTTPException(status_code=404, detail="Item not found")
