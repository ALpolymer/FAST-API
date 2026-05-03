from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from db import create_db_and_tables, get_session
from models import Hero,HeroUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    print("Database ready [OK]")

    yield

    print("Shutting down...")


app = FastAPI(title="Hero API - CRUD with SQL model", lifespan = lifespan)

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/heroes", response_model=Hero)
def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes")
def list_heroes(session: SessionDep, skip : int = 0, limit: int =10):
    statement = select(Hero)
    statement = statement.offset(skip).limit(limit)
    results = session.exec(statement)
    return results.all()
    # return session.exec(select(Hero).offset(skip).limit(limit).all())


@app.get("/heroes/{hero_id}", response_model = Hero)
def get_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, "Hero not found")
    return hero

@app.patch("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, patch: HeroUpdate, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, "Hero not found")
    update_data = patch.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(hero, field, value)
    
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, "Hero not found")
    session.delete(hero)
    session.commit()