from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, repositories
from ..database import get_db

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"]
)

@router.post("/", response_model=schemas.AddressRead)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return repositories.AddressRepository(db).create(address)


@router.get("/", response_model=List[schemas.AddressRead])
def list_addresses(db: Session = Depends(get_db)):
    return repositories.AddressRepository(db).list()


@router.get("/{address_id}", response_model=schemas.AddressRead)
def get_address(address_id: int, db: Session = Depends(get_db)):
    obj = repositories.AddressRepository(db).get(address_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return obj


@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    repositories.AddressRepository(db).delete(address_id)
    return {"ok": True}

