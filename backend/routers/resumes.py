from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, auth
from database import get_db


router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("", response_model=schemas.ResumeOut)
def create_resume(
    resume: schemas.ResumeCreate,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    return crud.create_resume(db, user.id, resume)

@router.get("", response_model=list[schemas.ResumeOut])
def list_resumes(
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    return crud.list_resumes(db, user.id)

@router.get("/{resume_id}", response_model=schemas.ResumeOut)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    resume = crud.get_resume(db, resume_id, user.id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.put("/{resume_id}", response_model=schemas.ResumeOut)
def update_resume(
    resume_id: int,
    resume_update: schemas.ResumeUpdate,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user)
):
    return crud.update_resume(db, resume_id, user.id, resume_update)

@router.get("/{resume_id}/improve", response_model=schemas.ResumeOut)
def improve_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    return crud.improve_resume(db, resume_id, user.id)

@router.delete("/{resume_id}")
def delete(
    resume_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    return crud.delete_resume(db, resume_id, user.id)
