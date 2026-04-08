from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    # PK
    id = Column(Integer, primary_key=True, index=True)

    # Données perso
    age = Column(Integer, nullable=False)
    situation_familiale = Column(String)
    niveau_etude = Column(String)
    sport_licence = Column(Boolean, default=False)
    date_creation_compte = Column(Date)

    # Relation vers le profil de risque (Principe Merise)
    # FK
    finance_id = Column(Integer, ForeignKey("finance.id"))
    finance = relationship("Finance", back_populates="user")

class Finance(Base):
    __tablename__ = "finance"

    # PK
    id = Column(Integer, primary_key=True, index=True)

    # Données financières
    revenu_estime_mois = Column(Float)
    loyer_mensuel = Column(Float)
    montant_pret = Column(Float)
    score_credit = Column(Float)
    risque_personnel = Column(Float)

    user = relationship("User", back_populates="finance", uselist=False)