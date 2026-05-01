from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field


app = FastAPI(title= "Status Codes")

class Item(BaseModel):
    name: str = Field(..., description="name of the item", examples=["Bag"])
    price: float = Field(..., description="The price of the item", examples=[8.5])

app.state.items_db = dict[int, Item] = {}
app.state.counter = 0

@app.post("/items", response_model=Item, status_code= status.HTTP_201_CREATED, tags=["Items"])
def create_item(item :Item):
    app.state.counter += 1
    app.state.items_db[app.state.counter] = item
    return item

@app.delete("items/{item_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
     app.state.items_db.pop(item_id, None)