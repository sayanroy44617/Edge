from fastapi import FastAPI
from .routes.node_router import router

app = FastAPI()

app.include_router(router)  # Assuming 'router' is imported from node_router.py