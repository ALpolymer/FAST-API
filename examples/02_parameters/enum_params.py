from fastapi import FastAPI
from enum import Enum

app = FastAPI(
    title= "Enum path params",
    version="1.0.1"
)

class Role(str, Enum):
    """
    Enum represeting the only valid user roles by the user roles accepted by the endpoint.

    Why inherit from both `str` and `Enum`:
    - `Enum` gives as a fixed set of allowed values
    - `str` makes enums behave like strings in many contexts

    Allowed values:
    - admin
    - editor
    - viewer
    """

    admin = "admin"
    editor = "editor"
    viewer = "viewer"

@app.get("/users/{role}")
def list_users(role : Role):
    return {
        "role": role,
        "message": f"Listing all {role.value}s"
    }