from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

items = {}


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


@app.post("/items/{item_id}", response_model=Item)
async def create_item(item_id: int, itme: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = itme
    return itme


@app.get("/items", response_model=List[Item])
async def read_items():
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
