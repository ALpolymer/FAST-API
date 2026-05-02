from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI(title="Simple Dependencies")

fake_items = [{"name": f"Item{i}"} for i in range(100)]
fake_users = [{"name": f"User{i}"} for i in range(100)]

# @app.get("/items")
# def list_items(skip: int=0, limit: int=10):
#     return fake_items[skip: skip+limit]   

# @app.get("/users")
# def list_users(skip: int=0, limit: int=10):
#     return fake_users[skip: skip+limit]   

def pagination(skip: int=0, limit: int=10):
    return{
        "skip": skip,
        "limit": limit
    }


# Create type alias for cleaner signatures
# dict as we defined above(pagination function returns a dict)

Page = Annotated[dict, Depends(pagination)]

@app.get("/items")
def list_items(page: Page):
    return fake_items[page["skip"]: page["skip"] + page["limit"]]   


@app.get("/users")
def list_users(page: Page):
    return fake_users[page["skip"]: page["skip"] + page["limit"]]   

fake_products = [
    {"name" : f"Product {i}", "category":"electronics" if i%2 == 0 else "clothing"} for i in range(80)
]

@app.get("/products")
def list_products(page: Page, category: str | None = None):
    results = fake_products
    if category:
        results = [p for p in results if p['category'] == category]

    return results[page["skip"]: page["skip"] + page["limit"]]

@app.get("/search/{collection}")
def search(collection: str, page: Page, q: str):
    """Search a collection by name, with pagination.
    /search/items?q=Item 5
    /search/users?q=User&skip=0&limit=3
    /search/products?q=Product&skip=10&limit=5
    """
    collections = {
        "items": fake_items,
        "users": fake_users,
        "products": fake_products,
    }
    if collection not in collections:
        raise HTTPException(status_code=404, detail=f"Unknown collection '{collection}'")
    matches = [d for d in collections[collection] if q.lower() in d["name"].lower()]

    return matches[page["skip"]: page["skip"] + page["limit"]]