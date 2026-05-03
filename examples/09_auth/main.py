from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

SECRET_KEY = "demo-secret=key"
ALGORITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./auth_demo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread" : False}
)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Models
class User(SQLModel, table = True):

    __tablename__  = "users"

    id: int | None = Field(default=None, primary_key= True)
    username : str = Field(unique= True, index=True)
    hashed_password : str
    is_admin : bool = False

class UserCreate(BaseModel):
    username : str
    password : str

# Security Helpers

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)

def create_access_token(sub: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": sub, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
      token: Annotated[str, Depends(oauth2_schema)],
      session: SessionDep  
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

# App ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Auth Demo", lifespan=lifespan)

@app.post("/register")
def register(data: UserCreate, session: SessionDep):
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        raise HTTPException(400, "Username already exists")
    username = data.username
    hashed_password = hash_password(data.password)
    is_admin = (data.username == "admin")
    user = User(username=username, hashed_password=hashed_password, is_admin=is_admin)

    session.add(user)
    session.commit()
    return { "ok" : True, "username": user.username}

@app.login("/login")
def login(
    form : Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer"
    }

@app.post("/me")
def me(user: CurrentUser):
    return{
        "username" : user.username,
        "is_admin" : user.is_admin
    }

@app.get("/admin")
def admin_only(user : CurrentUser):
    if not user.is_admin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Admins only")
    return {
        "secret" : "42",
        "message" : f"Welcome , admin {user.username}!"
    }