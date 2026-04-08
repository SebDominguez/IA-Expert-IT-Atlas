from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

from .database import SessionLocal
from .models import User, Finance

app = FastAPI(title="API")

class FinanceCreate(BaseModel):
    revenu_estime_mois: float
    loyer_mensuel: float
    montant_pret: float
    score_credit: float

class UserCreate(BaseModel):
    age: int
    situation_familiale: str
    niveau_etude: str
    sport_licence: bool = False
    finance: FinanceCreate # On imbrique les finances ici

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- GET ---
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.finance)).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- POST ---
@app.post("/users/", status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # 1. Création de l'objet Finance
        new_finance = Finance(**user_data.finance.model_dump())
        db.add(new_finance)
        db.flush() # Récupère l'ID de finance sans valider la transaction

        # 2. Création de l'User lié à cette finance
        user_dict = user_data.model_dump(exclude={'finance'})
        new_user = User(**user_dict, finance_id=new_finance.id)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": "success",
            "message": "Utilisateur et profil financier créés",
            "user_id": new_user.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création : {str(e)}")

# --- DELETE ---
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}