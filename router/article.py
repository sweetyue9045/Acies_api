from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from router.schemas import ArticleRequestSchema, ArticleResponseSchema, UpdateResponseSchema
from db.database import get_db
from db import db_article
from typing import List
from fastapi import  File, UploadFile
import os
from os import getcwd, remove
from fastapi.responses import FileResponse,JSONResponse

router = APIRouter(
    prefix="/api/v1/article",
    tags=["article"]
)


@router.post("", response_model=ArticleResponseSchema)
def create(request: ArticleRequestSchema, db: Session = Depends(get_db)):
    return db_article.create(db=db, request=request)


@router.get("/feed", response_model=List[ArticleResponseSchema])
def feed_initial_articles(db: Session = Depends(get_db)):
    return db_article.db_feed(db)


@router.get("/all", response_model=List[ArticleResponseSchema])
def get_all_articles(db: Session = Depends(get_db)):
    return db_article.get_all(db)


@router.get("/id/{id}", response_model=ArticleResponseSchema)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    return db_article.get_article_by_id(id=id, db=db)


@router.get("/{category}", response_model=List[ArticleResponseSchema])
def get_article_by_category(category: str, db: Session = Depends(get_db)):
    return db_article.get_article_by_category(category=category, db=db)

@router.put("/id/{user_id}/update")
def update_user(user_id: int, request: UpdateResponseSchema, db: Session = Depends(get_db)):
    return db_article.update(user_id=user_id, db=db, request=request)

@router.delete("/id/{id}/delete", response_model=ArticleResponseSchema)
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_article.delete(id=id, db=db)

@router.post("/upload/", summary="上傳圖片")
async def upload_file(files: UploadFile = File(...)):
    dir_name = "im"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(f"{dir_name}/{files.filename}", 'wb') as image:
        content = await files.read()
        image.write(content)
        image.close()
    return {"filename": files}
    
@router.get("/file/{name_file}")
def get_file(name_file: str):
    dir_name = "/im"
    return FileResponse(path=getcwd() + dir_name + "/" + name_file)

@router.delete("/delete/file/{name_file}",  summary="刪除圖片")
def delete_file(name_file: str):
    dir_name = "/im"
    try:
        remove(getcwd() + dir_name + "/" + name_file)
        return JSONResponse(content={
            "removed": True
            }, status_code=200)   
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "error_message": "File not found"
        }, status_code=404)