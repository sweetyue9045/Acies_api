from fastapi import HTTPException, status
from router.schemas import ArticleRequestSchema, UpdateResponseSchema,PublishResponseSchema
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from .article_feed import article

from db.models import DbArticle

def db_feed(db: Session):
    new_article_list = [DbArticle(
        category=article["category"],
        img=article["img"],
        title=article["title"],
        content=article["content"],
        writer=article["writer"],
        write_time=article["write_time"],
        editer=article["editer"],
        edit_time=article["edit_time"],
        ispin=article["ispin"],
        ispublish=article["ispublish"]
    ) for article in article]
    db.query(DbArticle).delete()
    db.commit()
    db.add_all(new_article_list)
    db.commit()
    return db.query(DbArticle).all()


def create(db: Session, request: ArticleRequestSchema) -> DbArticle:
    new_article = DbArticle(
        category=request.category,
        img=request.img,
        title=request.title,
        content=request.content,
        writer=request.writer,
        write_time=request.write_time,
        editer=request.editer,
        edit_time=request.edit_time,
        ispin=request.ispin,
        ispublish=request.ispublish
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def update(id: int, db: Session, request: UpdateResponseSchema):
    user = db.query(DbArticle).filter(DbArticle.id == id)
    user.update({
        DbArticle.category: request.category,
        DbArticle.img: request.img,
        DbArticle.title: request.title,
        DbArticle.content: request.content,
        DbArticle.editer: request.editer,
        DbArticle.edit_time: request.edit_time
    })

    db.commit()
    return {
        'id': id,
        'category': request.category,
        'img': request.img,
        'title': request.title,
        'content': request.content,
        'editer': request.editer,
        'edit_time': request.edit_time
    }

def delete(id: int, db: Session) -> list[DbArticle]:
    article = db.query(DbArticle).get(id)
    db.delete(article)
    db.commit()


def get_all(db: Session) -> list[DbArticle]:
    return db.query(DbArticle).all()


def get_article_by_id(id: int, db: Session) -> DbArticle:
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Article with id = {id} not found')
    return article

def get_article_by_category(category: str, db: Session) -> list[DbArticle]:
    article = db.query(DbArticle).filter(func.upper(DbArticle.category) == category.upper()).all()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with category = {category} not found')
    return article

def publish(id: int, db: Session, request: PublishResponseSchema):
    user = db.query(DbArticle).filter(DbArticle.id == id)
    user.update({
        DbArticle.ispublish: request.ispublish
    })

    db.commit()
    return {
        'id': id,
        'ispublish': request.ispublish
    }