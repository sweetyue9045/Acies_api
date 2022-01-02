from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from router.schemas import ArticleRequestSchema, ArticleResponseSchema, UpdateResponseSchema,PublishResponseSchema
from db.database import get_db
from db import db_article
from typing import List
from fastapi import  File, UploadFile
from starlette.responses import StreamingResponse
from os import getcwd
from fastapi.responses import FileResponse,JSONResponse
import os
from os import getcwd, remove

router = APIRouter(
    prefix='/api/v1/article',
    tags=['article']
)


@router.post('', response_model=ArticleResponseSchema)
def create(request: ArticleRequestSchema, db: Session = Depends(get_db)):
    return db_article.create(db=db, request=request)


@router.get('/feed', response_model=List[ArticleResponseSchema])
def feed_initial_articles(db: Session = Depends(get_db)):
    return db_article.db_feed(db)


@router.get('/all', response_model=List[ArticleResponseSchema],summary="獲得文章")
def get_all_articles(db: Session = Depends(get_db)):
    return db_article.get_all(db)


@router.get('/id/{id}', response_model=ArticleResponseSchema)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    return db_article.get_article_by_id(id=id, db=db)


@router.get("/{category}", response_model=List[ArticleResponseSchema])
def get_article_by_category(category: str, db: Session = Depends(get_db)):
    return db_article.get_article_by_category(category=category, db=db)

@router.put('/id/{id}/update',summary="更新文章")
def update_article(id: int, request: UpdateResponseSchema, db: Session = Depends(get_db)):
    return db_article.update(id=id, db=db, request=request)

@router.delete('/id/{id}/delete', response_model=ArticleResponseSchema,summary="刪除文章")
def delete_article(id: int, db: Session = Depends(get_db)):
    return db_article.delete(id=id, db=db)

@router.put('/id/{id}/publish',summary="發佈文章")
def publush(id: int, request: PublishResponseSchema, db: Session = Depends(get_db)):
    return db_article.publish(id=id, db=db, request=request)

@router.post("/upload/", summary="上傳圖片")
async def upload_file(files: UploadFile = File(...)):
    dir_name = "im"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(f"im/{files.filename}", 'wb') as image:
        content = await files.read()
        image.write(content)
        image.close()
    return {"filename": files}
    
@router.get("/file/{name_file}",summary="獲得圖片網址")
def get_file(name_file: str):
    dir_name = "/im"
    return FileResponse(path=getcwd() + dir_name + "/" + name_file)

@router.delete("/delete/file/{name_file}",summary="刪除圖片")
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