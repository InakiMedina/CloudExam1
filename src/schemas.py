
from pydantic import BaseModel, ConfigDict
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
    
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    unit: Optional[str] = None
    base_price: float


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)

class NoteItemCreate(BaseModel):
    product_id: int
    quantity: int

class NoteItemRead(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    total: float
    
    model_config = ConfigDict(from_attributes=True)

class SalesNoteRead(BaseModel):
    id: int
    folio: str
    client_id: int
    fac_address_id: int
    send_address_id: int
    total: float
    contents: List[NoteItemRead] 

    model_config = ConfigDict(from_attributes=True)

class SalesNoteCreate(BaseModel):
    folio: str
    client_id: int
    fac_address_id: int
    send_address_id: int
    items: List[NoteItemCreate]