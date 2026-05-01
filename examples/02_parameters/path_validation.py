from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI(
    title="Path Validation",
    version="1.0.1"
)

@app.get("/items/{item_id}", tags=["Items"])
def get_item(item_id: Annotated[int, Path(
    ge=1 ,
    le=10_000,
    examples=[44]

)]):
    """
    Return an item identifier after validation.

    `Path(...)` adds both validation rules and API documentation metadata.

    In this example:
    - `ge=1` means the value must be greater than or equal to 1
    - `le=10_000` means the value must be less than or equal to 10,000
    - `description` appears in the generated docs
    - `examples` helps document valid sample input

    FastAPI uses both:
    - the Python type hint (`int`) for type validation/conversion
    - the `Path(...)` metadata for extra constraints and docs

    Example:
        /items/5       -> valid
        /items/0       -> invalid (too small)
        /items/99999   -> invalid (too large)
    """
    return {"item_id" : item_id}