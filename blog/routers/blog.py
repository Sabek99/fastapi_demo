from typing import List
from fastapi import APIRouter, Depends,status
from .. import schemas, database
from sqlalchemy.orm import Session
from..repository import blog




router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
def getAll(db:Session = Depends(get_db)):
    return blog.get_all(db)


@router.get('/{id}', status_code=200, response_model= schemas.ShowBlog)
def getBlog(id : int, db:Session = Depends(get_db)):
    return blog.getById(id,db)


@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schemas.BLog, db:Session = Depends(get_db)):
    return blog.create(request,db)


@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def updateBlog(id:int, request:schemas.BLog, db:Session = Depends(get_db)):
    return blog.update(id,request,db)


@router.delete('/{id}',status_code =status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int,db:Session = Depends(get_db)):
    return blog.delete(id,db)
    

