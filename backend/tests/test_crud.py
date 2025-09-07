import pytest
from sqlalchemy.orm import Session
import crud
import schemas
from auth import get_password_hash


def test_create_user(db: Session):
    user = crud.create_user(db, "testuser@example.com", get_password_hash("secret123"))
    assert user.id is not None
    assert user.email == "testuser@example.com"


def test_get_user(db: Session):
    user = crud.create_user(db, "joan@example.com", get_password_hash("secret123"))
    fetched = crud.get_user_by_email(db, "joan@example.com")
    assert fetched is not None
    assert fetched.email == "joan@example.com"


def test_create_resume(db: Session):
    user = crud.create_user(db, "resume_user@example.com", get_password_hash("pass123"))

    resume_in = schemas.ResumeCreate(
        title="Backend Developer",
        content="Опыт разработки на Python и FastAPI"
    )
    resume = crud.create_resume(db, user.id, resume_in)

    assert resume.id is not None
    assert resume.title == "Backend Developer"
    assert resume.owner_id == user.id


def test_update_resume(db: Session):
    user = crud.create_user(db, "resume_updater@example.com", get_password_hash("pass123"))

    resume_in = schemas.ResumeCreate(title="Junior Dev", content="Без опыта")
    resume = crud.create_resume(db, user.id, resume_in)

    update_in = schemas.ResumeUpdate(title="Middle Dev", content="1 год опыта")
    updated = crud.update_resume(db, resume.id, user.id, update_in)

    assert updated.title == "Middle Dev"
    assert updated.content == "1 год опыта"


def test_delete_resume(db: Session):
    user = crud.create_user(db, "resume_deleter@example.com", get_password_hash("pass123"))

    resume_in = schemas.ResumeCreate(title="Temporary Resume", content="На удаление")
    resume = crud.create_resume(db, user.id, resume_in)

    deleted = crud.delete_resume(db, resume.id, user.id)

    fetched = crud.get_resume(db, resume.id, user.id)
    assert fetched is None
