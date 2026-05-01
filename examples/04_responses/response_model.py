from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI(title= "Response Model")

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr

users_db = list[dict] = []

@app.post("/users", response_model = UserOut)
def create_user(user: UserIn):
    users_db.append(user)
    return user