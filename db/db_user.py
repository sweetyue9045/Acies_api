from fastapi import HTTPException, status
from router.schemas import UserRequestSchema, SignInRequestSchema
from sqlalchemy.orm.session import Session
from sqlalchemy import func, exc
from sqlalchemy.exc import IntegrityError
from db.models import DbUser
from utils.hash import bcrypt, verify


def register(db: Session, request: UserRequestSchema) -> DbUser:
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=bcrypt(request.password),
        is_admin=request.is_admin,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"{exc}".split("\n")[0])


def signin(db: Session, request: SignInRequestSchema):
    user = db.query(DbUser).filter(func.upper(DbUser.email) == request.email.upper()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email = {request.email} not found")
    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")
    return user


def get_all_users(db: Session) -> list[DbUser]:
    users = db.query(DbUser).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Users not found")
    return users


def get_user_by_id(user_id: int, db: Session) -> DbUser:
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {user_id} not found")
    return user


def get_user_by_email(user_email: str, db: Session) -> DbUser:
    user = db.query(DbUser).filter(func.upper(DbUser.email) == user_email.upper()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email = {user_email} not found")
    return user
