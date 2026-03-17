
from pydantic import BaseModel
from typing import List, Optional

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
