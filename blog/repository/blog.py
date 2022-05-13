
from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status

def get_all(db:Session):
     return db.query(models.Blog).all()


def create(request : schemas.BLog, db:Session):
     new_blog = models.Blog(title = request.title, body = request.body, user_id=1)
     db.add(new_blog)
     db.commit()
     db.refresh(new_blog)
     return new_blog 


def delete(id:int, db:Session):
     blog = db.query(models.Blog).filter(models.Blog.id == id)

     if not blog.first():
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with this Id:{id} is not found!" )

     blog.delete(synchronize_session=False)
     db.commit()
     return 'blog has been deleted!'


def update(id:int, request:schemas.BLog,db:Session):
     blog = db.query(models.Blog).filter(models.Blog.id == id)

     if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,details = f'Blog with Id {id} was not found!')
    
     blog.update({ models.Blog.body:request.body,models.Blog.title:request.title})
     db.commit()
     return 'blog has been updated!'


def getById(id:int, db:Session):
     blog =  db.query(models.Blog).filter(models.Blog.id == id).first()
     if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with this Id:{id} is not found!" )
     
     return blog