from datetime import date
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/posts')
def index(limit:int = 10, published:bool = True):
    if published:
        return {'data':f'{limit} published posts from the db'}
    else:
        return {'data':f'{limit} posts ' }
        

@app.get('/about')
def about():
    return {'data':{'about page'}}



@app.get('/post/details')
def getPostById():
    return{'data':"this post was posted by bla bla bla"}


@app.get('/post/{id}')
def getPostById(id:int):
    return{'data':id}

class Post(BaseModel):
    userId: int
    body: str
    publishedDate: date

@app.post('/post')
def create_post(post:Post):
    return{}