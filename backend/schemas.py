from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr

class NewsletterCreate(BaseModel):
    title: str
    content: str
