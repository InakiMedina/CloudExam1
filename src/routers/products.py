from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, repositories
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return repositories.ProductRepository(db).create(product)


@router.get("/", response_model=List[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return repositories.ProductRepository(db).list()


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = repositories.ProductRepository(db).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    repositories.ProductRepository(db).delete(product_id)
    return {"ok": True}
