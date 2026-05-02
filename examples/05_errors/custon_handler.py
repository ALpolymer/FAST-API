from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Custom Exception Handler")

class BusinessError(Exception):
    def __init__(self, code: str, msg: str):
        self.code = code
        self.msg = msg

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=422,
        content={
            "code": exc.code,
            "message": exc.msg
        }
    )

@app.post("/orders")
def place_order(n: int):
    if n<=0: 
        raise BusinessError("INVALID QUANTITY", "Quantity must be positive")
    return {
        "ok": True,
        "quantity": n
    }