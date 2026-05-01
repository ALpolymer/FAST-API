from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Request Bodies - Basics")

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    tags : list[str] = Field(default_factory=list)

items = list[Item] = []

@app.post("/items")
def create_item(item : Item):
    items.append(item)
    return { "ok": True, "item": item}

@app.get("/items")
def get_items():
    """Return all items"""
    return {"items" : items}

@app.get("/demo")
def demo():
    """Show how model_dump converts a model to a dictionary"""
    item = Item(name="Book", price = 19.99)
    return item.model_dump()