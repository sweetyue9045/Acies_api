from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.schema import ForeignKey

class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=True)

class DbArticle(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    img = Column(String)
    title = Column(String)
    content = Column(String)
    writer = Column(String)
    write_time = Column(String)
    editer = Column(String)
    edit_time = Column(String)
    ispin= Column(Boolean, default=False, nullable=False)
    ispublish= Column(Boolean, default=False, nullable=False)