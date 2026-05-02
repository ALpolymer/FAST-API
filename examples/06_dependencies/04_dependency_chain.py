from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

app = FastAPI(title= "Depedency Chain")

# Depedency 1 : verify token
def get_token(x_token: Annotated[str, Header()]) -> str:
    if x_token != "secret":
        raise HTTPException(401, "Invalid token")
    return x_token

#Dep 2: depends on dep1
def get_current_user(token: Annotated[str, Depends(get_token)]) -> dict:
    return {
        "username": "Alice",
        "token": token
    }

CurrentUser = Annotated[dict, Depends(get_current_user)]

@app.get("/me")
def me(user: CurrentUser):
    return user

@app.get("/admin")
def admin(user: CurrentUser):
    return {
        "message" : f"Welcome admin {user['username']}"
    }