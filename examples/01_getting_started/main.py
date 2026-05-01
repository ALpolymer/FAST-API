from fastapi import FastAPI

# https://127.0.0.1:8000/docs

#Create the FastAPI app instance
app = FastAPI(
    title= "Hello FastAPI",
    description="Our fisrt FastAPI app",
    version="1.0.1"
)

@app.get("/")
def read_root():
    """Return a simple Greeting"""
    return {"message":"Hello FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Read a single item by it's ID

    the type hint `int` tells FastAPI to:
    - Validate that item_id is an integer
    - Convert the string from url to an int
    - Return 422 if valifation fails
    """
    return{
        "item_id": item_id,
        "name": f"Item #{item_id}"
    }