from fastapi import FastAPI
from .routes.node_router import router
from .db.database import create_db_and_tables

app = FastAPI()
create_db_and_tables()

app.include_router(router)