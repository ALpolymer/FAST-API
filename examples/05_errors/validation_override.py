from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Validation Override")

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code= 400,
        content={
            "error": "Invalid Request",
            "issues": [
                {
                    "field": ".".join(map(str, e["loc"][1:])),
                    "msg": e['msg']
                }
                for e in exc.errors()
            ],
        },
    )

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id
    }