from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title= "Body + Path + Query")

class Item(BaseModel):
    name: str
    price: float
    in_stock : bool = True

@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    notify: bool = False
): return{
    "item_id": item_id,
    "item" : item,
    "notify": notify    
}