import os
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, database, repositories
from .services.aws_service import AWSService
from . import schemas

from .routers import clients, addresses, products, salesnotes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SalesNotes API")

# Include the routers
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(addresses.router)
# app.include_router(salesnotes.router)

# ----- sales note endpoint -----
@app.post("/salesnotes/", response_model=schemas.SalesNoteRead)
def create_salesnote(note: schemas.SalesNoteCreate, db: Session = Depends(database.get_db)):
    # create the note and its lines
    sn_repo = repositories.SalesNoteRepository(db)
    note_obj = sn_repo.create_with_items(note)

    client = repositories.ClientRepository(db).get(note.client_id)
  
    pdf_buf = aws_service.generate_pdf(note_obj, client, note_obj.contents)
    bucket = os.getenv("S3_BUCKET_NAME")
    aws_service.upload_pdf(pdf_buf, bucket, client.rfc, note_obj.folio)
    aws_service.send_notification(
        client.email,
        "Nueva nota de venta",
        f"Se ha generado la nota con folio {note_obj.folio}",
    )
    return note_obj
