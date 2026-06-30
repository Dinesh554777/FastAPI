from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Dinesh@30112006',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successfull") 
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error",error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}


my_posts=[{"title": "My posts", "content":"My posts content", "id": 3},{"title": "My foods", "content":"My favourite foods", "id": 1},{"title": "My cars", "content":"My favourite cars", "id": 5}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_of_posts(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)


