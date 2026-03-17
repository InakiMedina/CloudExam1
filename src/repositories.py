from typing import List, Optional
from sqlalchemy.orm import Session

from . import models


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class ClientRepository(BaseRepository):
    def create(self, data):
        obj = models.Client(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, client_id: int) -> Optional[models.Client]:
        return self.db.get(models.Client, client_id)

    def list(self) -> List[models.Client]:
        return self.db.query(models.Client).all()

    def delete(self, client_id: int) -> None:
        obj = self.get(client_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()


class ProductRepository(BaseRepository):
    def create(self, data):
        obj = models.Product(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, product_id: int) -> Optional[models.Product]:
        return self.db.get(models.Product, product_id)

    def list(self) -> List[models.Product]:
        return self.db.query(models.Product).all()

    def delete(self, product_id: int) -> None:
        obj = self.get(product_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()


class AddressRepository(BaseRepository):
    def create(self, data):
        obj = models.Address(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, address_id: int) -> Optional[models.Address]:
        return self.db.get(models.Address, address_id)

    def list(self) -> List[models.Address]:
        return self.db.query(models.Address).all()

    def delete(self, address_id: int) -> None:
        obj = self.get(address_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()


class SalesNoteRepository(BaseRepository):
    def create_with_items(self, data) -> models.SalesNote:
        """Accepts a Pydantic object with items attribute."""
        note = models.SalesNote(
            folio=data.folio,
            client_id=data.client_id,
            fac_address_id=data.fac_address_id,
            send_address_id=data.send_address_id,
        )
        self.db.add(note)
        self.db.flush()  # get id without committing
        total = 0
        for item in data.items:
            line_total = item.unit_price * item.quantity
            content = models.NoteContent(
                note_id=note.id,
                product_id=item.product_id,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total=line_total,
            )
            self.db.add(content)
            total += line_total
        note.total = total
        self.db.commit()
        self.db.refresh(note)
        return note

    def get(self, note_id: int) -> Optional[models.SalesNote]:
        return self.db.get(models.SalesNote, note_id)

    def list(self) -> List[models.SalesNote]:
        return self.db.query(models.SalesNote).all()
