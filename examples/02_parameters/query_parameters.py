"""
02 — Query Parameters: Basics, Defaults, Optional

This example introduces the most common FastAPI query parameter patterns:

1. Basic query parameters
   Any function parameter not declared in the path is treated as a query parameter.

2. Default values
   A default value makes a query parameter optional.

3. Optional parameters with validation
   Query(...) lets you attach validation rules and documentation metadata.

4. Automatic type conversion
   FastAPI converts incoming query string values to Python types based on type hints.

Run:
    uvicorn examples.02_parameters.query_params:app --reload

Alternative:
    fastapi dev query_params.py

Open API docs:
    http://localhost:8000/docs

Try:
    GET /items
        -> skip=0, limit=10

    GET /items?limit=5
        -> skip=0, limit=5

    GET /items?skip=20&limit=5

    GET /search?q=fastapi&in_stock=true

    GET /search
        -> q=None
"""

# To run this code:
# fastapi dev query_params.py
# or
# uvicorn query_params:app --reload
# To view the Swagger UI documentation:
# http://localhost:8000/docs

from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI(
    title="query parameters",
    version="1.0.1"
)

fake_items = [
    {"name": f"Item-{i}"} for i in range(100)
]

@app.get("/items", tags=["Items"])
def list_items(skip: int =0, limit: int = 10):
    """
    Return a slice of the fake items list.

    Key idea:
    Any function parameter that is not part of the path is interpreted
    by FastAPI as a query parameter.

    Here:
    - `skip` defaults to 0
    - `limit` defaults to 10

    Because both have default values, they are optional.

    Example requests:
        /items
        /items?limit=5
        /items?skip=20&limit=5

    FastAPI also converts query string values automatically:
        ?skip=20   -> int
        ?limit=5   -> int
    """
    return{
        "skip": skip,
        "limit": limit,
        "count" : len(fake_items[skip: skip + limit]),
        "items" : fake_items[skip: skip + limit]
    }


@app.get("/search")
def search(
        q: Annotated[
            str | None, 
            Query(
                min_length=3,
                max_length=50,
                description="Search query string",
                examples=["fastapi"]
            )            
        ] = None,
        category: Annotated[
            str,
            Query(
                description="Category search in. Defaults to `all`",
                examples=["books"]
            )
        ] = "all",
        in_stock: Annotated[
            bool,
            Query(
                description= "Whether to return only in-stock items",
                example=["True"]
            )
        ] = False
):
    return {
        "q": q,
        "category": category,
        "in_stock": in_stock
    }