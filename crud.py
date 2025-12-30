from sqlalchemy.orm import Session
import models
import schemas
from auth import get_password_hash
from datetime import datetime
from typing import List, Optional

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Property CRUD
def get_property(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()

def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Property).offset(skip).limit(limit).all()

def create_property(db: Session, property: schemas.PropertyCreate, owner_id: int):
    db_property = models.Property(**property.dict(), owner_id=owner_id)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, property_id: int, property_update: schemas.PropertyCreate, owner_id: int):
    db_property = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.owner_id == owner_id
    ).first()
    if not db_property:
        return None
    
    for key, value in property_update.dict().items():
        setattr(db_property, key, value)
    
    db.commit()
    db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int, owner_id: int):
    db_property = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.owner_id == owner_id
    ).first()
    if not db_property:
        return False
    
    db.delete(db_property)
    db.commit()
    return True

def get_user_properties(db: Session, owner_id: int):
    return db.query(models.Property).filter(models.Property.owner_id == owner_id).all()

# Booking CRUD
def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    # Calculate total price
    property = get_property(db, booking.property_id)
    if not property:
        return None
    
    # Calculate number of days
    days = (booking.check_out - booking.check_in).days
    if days <= 0:
        days = 1
    
    total_price = days * property.price_per_night
    
    db_booking = models.Booking(
        **booking.dict(),
        user_id=user_id,
        total_price=total_price,
        status="pending"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(db: Session, booking_id: int, booking_update: schemas.BookingCreate, user_id: int):
    db_booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id,
        models.Booking.user_id == user_id
    ).first()
    if not db_booking:
        return None
    
    # Recalculate price if dates changed
    if booking_update.check_in or booking_update.check_out:
        property = get_property(db, db_booking.property_id)
        days = (booking_update.check_out - booking_update.check_in).days
        db_booking.total_price = days * property.price_per_night
    
    for key, value in booking_update.dict().items():
        setattr(db_booking, key, value)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int, user_id: int):
    db_booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id,
        models.Booking.user_id == user_id
    ).first()
    if not db_booking:
        return False
    
    db.delete(db_booking)
    db.commit()
    return True

def get_user_bookings(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

# Favorite CRUD
def get_favorite(db: Session, favorite_id: int):
    return db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()

def get_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

def create_favorite(db: Session, favorite: schemas.FavoriteCreate, user_id: int):
    # Check if already favorited
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == user_id,
        models.Favorite.property_id == favorite.property_id
    ).first()
    
    if existing:
        return existing
    
    db_favorite = models.Favorite(**favorite.dict(), user_id=user_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, favorite_id: int, user_id: int):
    db_favorite = db.query(models.Favorite).filter(
        models.Favorite.id == favorite_id,
        models.Favorite.user_id == user_id
    ).first()
    if not db_favorite:
        return False
    
    db.delete(db_favorite)
    db.commit()
    return True