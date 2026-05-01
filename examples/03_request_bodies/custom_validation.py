from fastapi import FastAPI
from pydantic import BaseModel, field_validator, model_validator

app = FastAPI(title= "Custom Validator")

class SignupData(BaseModel):
    username: str
    password: str
    confirm_password : str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if len(v) < 8 or v.isalpha():
            raise ValueError("Password must be 8+ characters and include non letter")
        return v
    
    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    


@app.post("/signup")
def signup(data: SignupData):
    return{
        "ok": True,
        "username": data.username,
        "data": data
    }
