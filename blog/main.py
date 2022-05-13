from typing import List
from pyexpat import model
from turtle import title
from unicodedata import name
from urllib import request
from fastapi import FastAPI,Depends,status,Response,HTTPException
from blog import hashing
from . import schemas, models,hashing
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
    

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request:schemas.BLog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs',response_model=List[schemas.ShowBlog],tags=['blogs'])
def getAll(db:Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get('/blog/{id}', status_code=200, response_model= schemas.ShowBlog,tags=['blogs'])
def getBlog(id, response:Response, db:Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with this Id:{id} is not found!" )
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{'details':f'blog with Id {id} is not found!'}

    return blog


@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED,tags=['blogs'])
def updateBlog(id, request:schemas.BLog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,details = f'Blog with Id {id} was not found!')
    
    blog.update({ models.Blog.body:request.body,models.Blog.title:request.title})
    db.commit()
    return 'blog has been updated!'


@app.delete('/blog/{id}',status_code =status.HTTP_204_NO_CONTENT,tags=['blogs'])
def deleteBlog(id,db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'blog has been deleted!'


@app.post('/user',response_model= schemas.ShowUser,status_code=status.HTTP_201_CREATED,tags=["users"])
def createUser(request:schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email,password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', response_model=List[schemas.ShowUser],tags=["users"])
def getUsers(db:Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get('/user/{id}', response_model= schemas.ShowUser,tags=["users"])
def getUser(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with this Id {id} is not found!") 
    return user

