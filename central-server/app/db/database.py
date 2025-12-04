from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Hero(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: Union[int, None] = Field(default=None, index=True)
    secret_name: str


SQLALCHEMY_DATABASE_URL = "postgresql://app_user:secure_password@postgres:5432/app_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def test_connection():
    # 4. Create the Table
    print("Creating table 'hero'...")
    SQLModel.metadata.create_all(engine)

    # 5. Insert Data
    print("Inserting a Hero...")
    hero_1 = Hero(name="EdgeFlow Man", secret_name="Agent 007")

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)
        print(f"Created Hero: {hero_1}")

    # 6. Read Data Back
    print("Reading data back...")
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "EdgeFlow Man")
        results = session.exec(statement)
        hero = results.first()

        if hero:
            print(f"✅ SUCCESS! Found hero: {hero.name} (Secret: {hero.secret_name})")
        else:
            print("❌ FAILURE! Could not find the hero we just added.")

if __name__ == "__main__":
    try:
        test_connection()
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")

