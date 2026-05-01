"""
02 — Path Parameters: Basics

This example introduces two common FastAPI path parameter patterns:

1. Standard typed path parameters
   Example:
       /users/42
   FastAPI validates and converts the value based on the Python type hint.

2. Catch-all path parameters using :path
   Example:
       /files/home/user/data.csv
   FastAPI captures the whole remaining URL path, including slashes.

Run:
    uvicorn examples.02_parameters.path_params:app --reload

Alternative:
    fastapi dev path_params.py

Open API docs:
    http://localhost:8000/docs

Try:
    GET /users/42
        -> {"user_id": 42, "kind": "int"}

    GET /users/abc
        -> 422 Unprocessable Entity

    GET /files/report.txt
        -> {"file_path": "report.txt"}

    GET /files/home/user/data.csv
        -> {"file_path": "home/user/data.csv"}
"""


# To run this code:
# fastapi dev path_params.py
# or
# uvicorn path_params:app --reload
# To view the Swagger UI documentation:
# http://localhost:8000/docs

from fastapi import FastAPI

app = FastAPI(
    title="Path parameters",
    description="Demonstrates how to validate path parameters",
    version= "1.0.0"
)

@app.get("/users/{user_id}",
         summary="Get a user by numeric id",
         description="Accepts a user id as a path parameter",
         tags=["users"]
         )
def get_user(user_id: int):
    """
    Return user identifier received from the url path,

    The type `int` is important because FastAPI uses it to:
    1. validate the incoming value is a valid integer.
    2. convert the path value from string to in automatically.
    3. reject invalid values before entering the function.   

    Example:

        /users/42  -> valid
        /users/abc -> invalid, returns 422
    """
    return{
        "user_id" : user_id,
        "kind": type(user_id).__name__
    }

@app.get("/files/{file_path:path}", tags=["Files"])
def read_file(file_path: str):
    return {"file_path" : file_path}