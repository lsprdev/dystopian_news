from sqlalchemy.orm import Session
from models import User, Newsletter
from schemas import UserCreate, NewsletterCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def create_newsletter(db: Session, newsletter: NewsletterCreate):
    db_newsletter = Newsletter(**newsletter.dict())
    db.add(db_newsletter)
    db.commit()
    db.refresh(db_newsletter)
    return db_newsletter
