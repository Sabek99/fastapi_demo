from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from .. import models, schemas, database
from sqlalchemy.orm import Session





router = APIRouter()
get_db = database.get_db

@router.get('/blogs',response_model=List[schemas.ShowBlog],tags=['blogs'])
def getAll(db:Session = Depends(get_db)):
    return db.query(models.Blog).all()




@router.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request:schemas.BLog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.get('/blog/{id}', status_code=200, response_model= schemas.ShowBlog,tags=['blogs'])
def getBlog(id, db:Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with this Id:{id} is not found!" )
    
    return blog


@router.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED,tags=['blogs'])
def updateBlog(id, request:schemas.BLog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,details = f'Blog with Id {id} was not found!')
    
    blog.update({ models.Blog.body:request.body,models.Blog.title:request.title})
    db.commit()
    return 'blog has been updated!'


@router.delete('/blog/{id}',status_code =status.HTTP_204_NO_CONTENT,tags=['blogs'])
def deleteBlog(id,db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'blog has been deleted!'

