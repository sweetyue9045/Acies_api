from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import UserResponseSchema, UserRequestSchema, SignInRequestSchema
from db.database import get_db
from db import  db_user
from typing import List

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)


@router.post("/register", response_model=UserResponseSchema)
async def register(request: UserRequestSchema, db: Session = Depends(get_db)):
    return db_user.register(db=db, request=request)


@router.post("/signin", response_model=UserResponseSchema)
async def signin(request: SignInRequestSchema, db: Session = Depends(get_db)):
    return db_user.signin(db=db, request=request)


@router.get("/id/{user_id}", response_model=UserResponseSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(user_id=user_id, db=db)


@router.get("/{user_email}", response_model=UserResponseSchema)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    return db_user.get_user_by_email(user_email=user_email, db=db)