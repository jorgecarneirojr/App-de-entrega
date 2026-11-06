from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.address import Address
from app.models.user import User
from app.schemas.address import AddressCreate, AddressUpdate
from app.services.geo import build_address_query, geocode

ADDRESS_FIELDS = {"street", "number", "district", "city", "state", "zip_code"}


def _apply_geocoding(address: Address) -> None:
    if not settings.GEOCODING_ENABLED:
        return
    if address.latitude is not None and address.longitude is not None:
        return
    result = geocode(build_address_query(address))
    if result:
        address.latitude = result["latitude"]
        address.longitude = result["longitude"]


def list_addresses(db: Session, user: User) -> list[Address]:
    return db.scalars(select(Address).where(Address.user_id == user.id).order_by(Address.id.desc())).all()


def create_address(db: Session, user: User, payload: AddressCreate) -> Address:
    address = Address(user_id=user.id, **payload.model_dump())
    _apply_geocoding(address)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(db: Session, user: User, address_id: int, payload: AddressUpdate) -> Address:
    address = db.scalar(select(Address).where(Address.id == address_id, Address.user_id == user.id))
    if not address:
        raise HTTPException(status_code=404, detail="Endereco nao encontrado")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(address, field, value)

    if ADDRESS_FIELDS.intersection(updates):
        address.latitude = updates.get("latitude")
        address.longitude = updates.get("longitude")
        _apply_geocoding(address)

    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, user: User, address_id: int) -> None:
    address = db.scalar(select(Address).where(Address.id == address_id, Address.user_id == user.id))
    if not address:
        raise HTTPException(status_code=404, detail="Endereco nao encontrado")

    db.delete(address)
    db.commit()
