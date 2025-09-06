from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List
from models import User, Resume, Improvement
from schemas import ResumeCreate, ResumeUpdate
from ai import improve_text


# Users

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password_hash: str) -> User:
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Resumes

def create_resume(db: Session, user_id: int, resume: ResumeCreate):
    db_resume = Resume(
        title=resume.title,
        content=resume.content,
        owner_id=user_id
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def list_resumes(db: Session, owner_id: int) -> List[Resume]:
    return db.query(Resume).filter(Resume.owner_id == owner_id).order_by(Resume.created_at.desc()).all()

def get_resume(db: Session, resume_id: int, owner_id: int) -> Optional[Resume]:
    return db.query(Resume).filter(Resume.id == resume_id, Resume.owner_id == owner_id).first()

def update_resume(db: Session, resume_id: int, owner_id: int, resume_update: ResumeUpdate):
    db_resume = get_resume(db, resume_id, owner_id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if db_resume.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this resume")

    # обновляем только то, что пришло
    if resume_update.title is not None:
        db_resume.title = resume_update.title
    if resume_update.content is not None:
        db_resume.content = resume_update.content

    db.commit()
    db.refresh(db_resume)
    return db_resume

def improve_resume(db: Session, resume_id: int, owner_id: int):
    db_resume = get_resume(db, resume_id, owner_id)
    # сохраняем прежнее резюме для истории
    imp = Improvement(resume_id=resume_id, content=db_resume.content)
    db_resume.content = improve_text(db_resume.content)

    db.add(imp)
    db.commit()
    db.refresh(imp)
    db.refresh(db_resume)

    return db_resume

def delete_resume(db: Session, resume_id: int, owner_id):
    db_resume = get_resume(db, resume_id, owner_id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if db_resume.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this resume")
    
    db.delete(db_resume)
    db.commit()
    
    return {"detail": "Resume deleted successfully"}
