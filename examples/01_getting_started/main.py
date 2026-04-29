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
    return {"message":"Hello FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return{
        "item_id": item_id,
        "name": f"Item #{item_id}"
    }