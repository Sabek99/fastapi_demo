
from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from .. import models, schemas, database
from sqlalchemy.orm import Session
from..repository import user


router = APIRouter(
    prefix="/user",
    tags=['Users']
)
get_db = database.get_db



@router.post('/',response_model= schemas.ShowUser,status_code=status.HTTP_201_CREATED)
def createUser(request:schemas.User, db:Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/', response_model=List[schemas.ShowUser])
def getUsers(db:Session = Depends(get_db)):
    return user.getAll(db)


@router.get('/{id}', response_model= schemas.ShowUser)
def getUser(id:int,db:Session = Depends(get_db)):
   return user.getUserById(id, db)


