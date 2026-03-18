from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from . import models, schemas


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
        try:
            # 1. Initialize Header
            note = models.SalesNote(
                folio=data.folio,
                client_id=data.client_id,
                fac_address_id=data.fac_address_id,
                send_address_id=data.send_address_id,
                total=0.0
            )
            self.db.add(note)
            self.db.flush() 

            total_accumulator = 0.0
            
            # 2. Process Items
            for item in data.items:
                product = self.db.get(models.Product, item.product_id)
                if not product:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Product {item.product_id} not found"
                    )
                
                # Use float to ensure math doesn't crash on Decimal types
                price = float(product.base_price) 
                line_total = price * item.quantity
                
                content = models.NoteContent(
                    note_id=note.id,
                    product_id=item.product_id,
                    unit_price=price,
                    quantity=item.quantity,
                    total=line_total,
                )
                self.db.add(content)
                total_accumulator += line_total
                
            # 3. Finalize Header
            note.total = total_accumulator
            self.db.commit()

            # 4. Return with Eager Loading
            return self.db.query(models.SalesNote)\
                .options(joinedload(models.SalesNote.contents))\
                .filter(models.SalesNote.id == note.id)\
                .first()

        except IntegrityError as e:
            self.db.rollback()
            # This catches duplicate Folios or Invalid Foreign Keys
            raise HTTPException(
                status_code=400, 
                detail=f"Database Integrity Error: {str(e.orig)}"
            )
        except HTTPException as http_e:
            self.db.rollback()
            raise http_e
        except Exception as e:
            self.db.rollback()
            # This catches everything else and tells you what happened
            raise HTTPException(
                status_code=500, 
                detail=f"Internal Server Error: {type(e).__name__} - {str(e)}"
            )

    def get(self, note_id: int) -> Optional[models.SalesNote]:
        return self.db.query(models.SalesNote)\
            .options(joinedload(models.SalesNote.contents))\
            .filter(models.SalesNote.id == note_id)\
            .first()

    def list(self) -> List[models.SalesNote]:
        return self.db.query(models.SalesNote)\
            .options(joinedload(models.SalesNote.contents))\
            .all()