from fastapi import FastAPI
from app.core.db import  engine, get_db, Base 
from app.routers.consent_routers import router as consent_router
from app.routers.legal_routers import router as legal_router
from app.consent.seed import seed_all
from app.consent.seed_users import seed_dummy_users
from app.models.users import User  
from app.models import users,user_consent,consent_master,audit_logs 

app = FastAPI(title="Consent Capture System")

app.include_router(consent_router)
app.include_router(legal_router)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def seed():
    db = next(get_db())
    seed_all(db)
    seed_dummy_users(db)

@app.get("/")
def root():
    return {"msg": "Consent Module Running"}
