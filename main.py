from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import crud
import models
import uvicorn
import schemas
import auth
from database import engine, get_db
from typing import List
import logging 
import os
from dotenv import load_dotenv

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Property Management API", docs_url="/docs", redoc_url="/redoc")

SECRET_KEY = os.getenv("SECRET_KEY")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                   "http://127.0.0.1:8000",  # Votre frontend local
        
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def root():
        html_content = """
        <html>
            <head><title>Bienvenue</title></head>
            <body>
                <h1>Bienvenu dans FASTAPI</h1>
                <p>Développé par NKONGA TADJUIDJE MOREL.</p>
                <p>Veuillez voir la docs de l'API en tapant <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a></p>
                <h4> c'est uniquement en local ici et si vous voulez clonez le projet le readme.md dans mon github est disponible</h4>

                <p> pour la production in faut cliquer sur ce lien https://property-management-api-gu02.onrender.com et pour voir la documentation en production click ici https://property-management-api-gu02.onrender.com/docs 
                Merci et bonne utilisation !</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# Authentication Endpoints
@app.post("/api/auth/registration/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/auth/login/", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/api/auth/logout/")
def logout():
    return {"message": "Successfully logged out"}

@app.get("/api/auth/user/", response_model=schemas.UserDetail)
def get_current_user_profile(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    user = crud.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Property Endpoints
@app.get("/api/properties/", response_model=List[schemas.Property])
def read_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    properties = crud.get_properties(db, skip=skip, limit=limit)
    return properties

@app.post("/api/properties/", response_model=schemas.Property, status_code=status.HTTP_201_CREATED)
def create_property(
    property: schemas.PropertyCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.create_property(db=db, property=property, owner_id=current_user.id)

@app.get("/api/properties/{property_id}/", response_model=schemas.PropertyDetail)
def read_property(property_id: int, db: Session = Depends(get_db)):
    db_property = crud.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@app.put("/api/properties/{property_id}/", response_model=schemas.Property)
def update_property(
    property_id: int,
    property_update: schemas.PropertyCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_property = crud.update_property(db, property_id=property_id, property_update=property_update, owner_id=current_user.id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found or not authorized")
    return db_property

@app.delete("/api/properties/{property_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_property(db, property_id=property_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found or not authorized")
    return None

# Booking Endpoints
@app.get("/api/bookings/", response_model=List[schemas.BookingDetail])
def read_bookings(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    bookings = crud.get_user_bookings(db, user_id=current_user.id)
    return bookings

@app.post("/api/bookings/", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: schemas.BookingCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check property availability
    property = crud.get_property(db, booking.property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if not property.is_available:
        raise HTTPException(status_code=400, detail="Property is not available")
    
    return crud.create_booking(db=db, booking=booking, user_id=current_user.id)

@app.get("/api/bookings/{booking_id}/", response_model=schemas.BookingDetail)
def read_booking(
    booking_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only allow booking owner to view
    if db_booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return db_booking

@app.put("/api/bookings/{booking_id}/", response_model=schemas.Booking)
def update_booking(
    booking_id: int,
    booking_update: schemas.BookingCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_booking = crud.update_booking(db, booking_id=booking_id, booking_update=booking_update, user_id=current_user.id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found or not authorized")
    return db_booking

@app.delete("/api/bookings/{booking_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_booking(db, booking_id=booking_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found or not authorized")
    return None

# Favorite Endpoints
@app.get("/api/favorites/", response_model=List[schemas.Favorite])
def read_favorites(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    favorites = crud.get_favorites(db, user_id=current_user.id)
    return favorites

@app.post("/api/favorites/", response_model=schemas.Favorite, status_code=status.HTTP_201_CREATED)
def create_favorite(
    favorite: schemas.FavoriteCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if property exists
    property = crud.get_property(db, favorite.property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return crud.create_favorite(db=db, favorite=favorite, user_id=current_user.id)

@app.delete("/api/favorites/{favorite_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    favorite_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_favorite(db, favorite_id=favorite_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found or not authorized")
    return None


if __name__ == "__main__":
    # Render fournit le port via la variable d'environnement PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)