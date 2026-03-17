from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.orm import relationship

from .database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    rfc = Column(String(13), unique=True, nullable=False)
    razon_social = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    comercial_name = Column(String(255))
    telefono = Column(String(20))

    sales_notes = relationship("SalesNote", back_populates="client")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    domicilio = Column(Text, nullable=False)
    colonia = Column(String(100))
    municipio = Column(String(100))
    estado = Column(String(100))
    address_type = Column(String(20))  # 'FACTURACIÓN'/'ENVÍO'

    billing_notes = relationship(
        "SalesNote", back_populates="fac_address", foreign_keys="SalesNote.fac_address_id"
    )
    shipping_notes = relationship(
        "SalesNote", back_populates="send_address", foreign_keys="SalesNote.send_address_id"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50))
    base_price = Column(DECIMAL(10, 2), nullable=False)

    note_contents = relationship("NoteContent", back_populates="product")


class SalesNote(Base):
    __tablename__ = "salesnotes"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String(50), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))
    fac_address_id = Column(Integer, ForeignKey("addresses.id"))
    send_address_id = Column(Integer, ForeignKey("addresses.id"))
    total = Column(DECIMAL(10, 2), default=0.00)

    client = relationship("Client", back_populates="sales_notes")
    fac_address = relationship(
        "Address",
        foreign_keys=[fac_address_id],
        back_populates="billing_notes",
    )
    send_address = relationship(
        "Address",
        foreign_keys=[send_address_id],
        back_populates="shipping_notes",
    )
    contents = relationship("NoteContent", back_populates="note", cascade="all, delete-orphan")


class NoteContent(Base):
    __tablename__ = "notecontent"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("salesnotes.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)

    note = relationship("SalesNote", back_populates="contents")
    product = relationship("Product", back_populates="note_contents")
