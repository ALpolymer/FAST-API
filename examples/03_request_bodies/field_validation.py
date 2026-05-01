from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title = "Field validation")

class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern=r"^[a-z0-9_]+$",
        description="Lowercase letters, numbers, and underscores only",
        examples=["john_doe"],
    )

    email: EmailStr = Field(
        ...,
        description="A valid email address",
        examples=["me@example.com"]
    )
    age : int = Field(
        ...,
        ge=18,
        le=150,
        description="Age must be between 18 and 50",
        examples=[20]
    )
    bio: str | None = Field(
        default= None,
        max_length=500,
        description="Optional short bio with 500 chars max",
        examples=["Python dev and ai enthusiast"]
    )

@app.post("/users", tags=["Users"])
def create_user(user: UserCreate):
    return {
        "user": user.model_dump(),
        "ok": True
    }