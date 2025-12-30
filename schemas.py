from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Property Schemas
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price_per_night: float
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    capacity: int = 1
    bedrooms: int = 1
    bathrooms: int = 1
    amenities: Optional[str] = None
    is_available: bool = True

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    property_id: int
    check_in: datetime
    check_out: datetime
    guests: int = 1
    special_requests: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Favorite Schemas
class FavoriteBase(BaseModel):
    property_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response schemas with relationships
class PropertyDetail(Property):
    owner: User
    bookings: List[Booking] = []

class BookingDetail(Booking):
    property: Property
    user: User

class UserDetail(User):
    properties: List[Property] = []
    bookings: List[Booking] = []
    favorites: List[Favorite] = []