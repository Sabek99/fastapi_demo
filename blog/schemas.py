import email
from typing import List
from unicodedata import name
from fastapi import Body
from pydantic import BaseModel

class BlogBase(BaseModel):
    title:str
    body:str

class BLog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name : str
    email : str
    blogs : List[BLog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator : ShowUser
    class Config():
        orm_mode = True