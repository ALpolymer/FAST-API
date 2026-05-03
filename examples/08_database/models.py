from sqlmodel import Field, Relationship, SQLModel

class Team(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    heroes : list["Hero"] = Relationship(back_populates="team")

#one_to_many relationship
class Hero(SQLModel, table =True):
    id: int | None = Field(default=None, primary_key=True)
    name : str = Field(index=True)
    age : int | None = None
    power : str | None = None
    # Foreign_key
    team_id: int | None = Field(default= None, foreign_key="team.id")
    team : Team | None = Relationship(back_populates="heroes")


# Schema
class HeroUpdate(SQLModel):
    name: str | None = None
    power: str | None = None
    age: str | None = None
    team_id = int | None = None