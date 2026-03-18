from typing import List

from fastapi import FastAPI
from sqlalchemy.orm import Session

from . import models, database

from .routers import clients, addresses, products, salesnotes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SalesNotes API")

# Include the routers
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(addresses.router)
app.include_router(salesnotes.router)
