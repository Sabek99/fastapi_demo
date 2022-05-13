
from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from blog import hashing
from .. import models, schemas, database
from sqlalchemy.orm import Session


router = APIRouter()
get_db = database.get_db





@router.post('/user',response_model= schemas.ShowUser,status_code=status.HTTP_201_CREATED,tags=["users"])
def createUser(request:schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email,password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user', response_model=List[schemas.ShowUser],tags=["users"])
def getUsers(db:Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get('/user/{id}', response_model= schemas.ShowUser,tags=["users"])
def getUser(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with this Id {id} is not found!") 
    return user

