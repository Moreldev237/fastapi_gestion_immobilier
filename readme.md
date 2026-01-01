# 🏠 API de Gestion de IMMOBILIERE developper avec FASTAPI

API REST complète pour la gestion de propriétés, réservations et favoris, construite avec FastAPI.

## ✨ Fonctionnalités

- 🔐 **Authentification** (Inscription/Connexion avec JWT)
- 🏠 **Gestion des propriétés** (CRUD complet)
- 📅 **Système de réservations**
- ⭐ **Gestion des favoris**
- 📚 **Documentation interactive automatique**
- 🔒 **Sécurité avancée** (Hash de mots de passe, Tokens JWT)
- 🎯 **Validation des données** avec Pydantic

## 🚀 Déploiement rapide

### Option : Render.com 
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy) 

### ou

 ### Option : pythonanywhere.com 
[![Deploy to pythonanywhere](https://pythonanywhere.com/images/deploy-to-pythonanywhere-button.svg)](https://pythonanywhere.com/deploy)


### Option pour ouvrir en Locale
```bash
# Cloner le projet
git clone https://github.com/Moreldev237/FASTAPI.git
cd FASTAPI

```bash
# Créer un environnement virtuel
python -m venv venv

```bash
# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

```bash
# Installer les dépendances
pip install -r requirements.txt

```bash
# Lancer le serveur
uvicorn main:app --reload

🌐 Documentation interactive

Une fois le serveur lancé, accédez à :

    Swagger UI : http://localhost:8000/docs

    ReDoc : http://localhost:8000/redoc

🛠️ Technologies utilisées

    FastAPI - Framework web moderne et rapide

    SQLAlchemy - ORM pour la base de données

    Pydantic - Validation des données

    JWT - Authentification par token

    bcrypt - Hashage des mots de passe

    CORS - Partage de ressources entre origines

📋 API Endpoints
🔐 Authentification


Méthode	  Endpoint  	Description
  POST	/api/auth/registration/	Inscription d'un nouvel utilisateur
  POST	/api/auth/login/	Connexion (obtention du token JWT)
  POST	/api/auth/logout/	Déconnexion
 GET	/api/auth/user/	Profil utilisateur

🏠 Propriétés
API Endpoints

Authentification


POST /api/auth/registration/ - Inscription
POST /api/auth/login/ - Connexion
POST /api/auth/logout/ - Déconnexion
GET /api/auth/user/ - Profil utilisateur
Propriétés

GET /api/properties/ - Liste des propriétés
POST /api/properties/ - Créer une propriété
GET /api/properties/{id}/ - Détails d'une propriété
PUT /api/properties/{id}/ - Modifier une propriété
DELETE /api/properties/{id}/ - Supprimer une propriété
Réservations

GET /api/bookings/ - Liste des réservations
POST /api/bookings/ - Créer une réservation
GET /api/bookings/{id}/ - Détails d'une réservation
PUT /api/bookings/{id}/ - Modifier une réservation
DELETE /api/bookings/{id}/ - Annuler une réservation
Favoris

GET /api/favorites/ - Liste des favoris
POST /api/favorites/ - Ajouter un favori
DELETE /api/favorites/{id}/ - Retirer un favori

Créé moi ses api avec FastAPI api

Voici une implémentation complète des API avec FastAPI :



1. Structure du projet
text

project/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
├── auth.py
└── requirements.txt


2. requirements.txt
txt

fastapi==0.104.1
uvicorn==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
