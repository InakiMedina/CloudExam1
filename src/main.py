import os
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models, database, repositories
from .services.aws_service import AWSService

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SalesNotes API")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ClientBase(BaseModel):
    rfc: str
    razon_social: str
    email: str
    comercial_name: Optional[str] = None
    telefono: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    unit: Optional[str] = None
    base_price: float


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    domicilio: str
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    address_type: Optional[str] = None


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    id: int

    class Config:
        orm_mode = True


class NoteItem(BaseModel):
    product_id: int
    unit_price: float
    quantity: int


class SalesNoteCreate(BaseModel):
    folio: str
    client_id: int
    fac_address_id: int
    send_address_id: int
    items: List[NoteItem]


class SalesNoteRead(BaseModel):
    id: int
    folio: str
    client_id: int
    fac_address_id: int
    send_address_id: int
    total: float

    class Config:
        orm_mode = True


aws_service = AWSService()

@app.post("/clients/", response_model=ClientRead)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    repo = repositories.ClientRepository(db)
    return repo.create(client)


@app.get("/clients/", response_model=List[ClientRead])
def list_clients(db: Session = Depends(get_db)):
    return repositories.ClientRepository(db).list()


@app.get("/clients/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    obj = repositories.ClientRepository(db).get(client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj


@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    repositories.ClientRepository(db).delete(client_id)
    return {"ok": True}


# ----- product endpoints -----
@app.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return repositories.ProductRepository(db).create(product)


@app.get("/products/", response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return repositories.ProductRepository(db).list()


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = repositories.ProductRepository(db).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    repositories.ProductRepository(db).delete(product_id)
    return {"ok": True}


# ----- address endpoints -----
@app.post("/addresses/", response_model=AddressRead)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return repositories.AddressRepository(db).create(address)


@app.get("/addresses/", response_model=List[AddressRead])
def list_addresses(db: Session = Depends(get_db)):
    return repositories.AddressRepository(db).list()


@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: int, db: Session = Depends(get_db)):
    obj = repositories.AddressRepository(db).get(address_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return obj


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    repositories.AddressRepository(db).delete(address_id)
    return {"ok": True}


# ----- sales note endpoint -----
@app.post("/salesnotes/", response_model=SalesNoteRead)
def create_salesnote(note: SalesNoteCreate, db: Session = Depends(get_db)):
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
