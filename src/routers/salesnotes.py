from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, repositories
from ..database import get_db

from ..services.aws_service import AWSService

router = APIRouter()

@router.post("/salesnotes/", response_model=schemas.SalesNoteRead)
def create_salesnote(note: schemas.SalesNoteCreate, db: Session = Depends(get_db)):
    # create the note and its lines
    sn_repo = repositories.SalesNoteRepository(db)
    note_obj = sn_repo.create_with_items(note)

    # client = repositories.ClientRepository(db).get(note.client_id)
  
    # pdf_buf = aws_service.generate_pdf(note_obj, client, note_obj.contents)
    # bucket = os.getenv("S3_BUCKET_NAME")
    # aws_service.upload_pdf(pdf_buf, bucket, client.rfc, note_obj.folio)
    # aws_service.send_notification(
    #     client.email,
    #     "Nueva nota de venta",
    #     f"Se ha generado la nota con folio {note_obj.folio}",
    # )
    return note_obj
