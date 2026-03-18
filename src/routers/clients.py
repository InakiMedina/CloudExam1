from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, repositories
from ..database import get_db

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.get("/", response_model=List[schemas.ClientRead])
def list_clients(db: Session = Depends(get_db)):
    return repositories.ClientRepository(db).list()


@router.post("/", response_model=schemas.ClientRead)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    repo = repositories.ClientRepository(db)
    return repo.create(client)


@router.get("/{client_id}", response_model=schemas.ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    obj = repositories.ClientRepository(db).get(client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    repositories.ClientRepository(db).delete(client_id)
    return {"ok": True}
