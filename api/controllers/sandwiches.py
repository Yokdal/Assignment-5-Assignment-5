from sqlalchemy.orm import Session
from .. import models
from fastapi import HTTPException, status

def create(db: Session, sandwich):
    db_sandwich = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def read_all(db: Session):
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return sandwich

def update(db: Session, sandwich_id: int, sandwich):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    update_data = sandwich.model_dump(exclude_unset=True)
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    return db_sandwich.first()

def delete(db: Session, sandwich_id: int):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Sandwich deleted successfully"}

