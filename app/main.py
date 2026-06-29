from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()

    return {"data":posts}


my_posts=[{"title": "My posts", "content":"My posts content", "id": 3},{"title": "My foods", "content":"My favourite foods", "id": 1},{"title": "My cars", "content":"My favourite cars", "id": 5}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_of_posts(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts= db.query(models.Post).all()

    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    
    # new_post=cursor.fetchone()
    # conn.commit()
    
    # new_post=models.Post(title=post.title, content=post.content, published=post.published)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    
    return {"data":new_post}

@app.get("/posts/{id}")
def get_one_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id)))
    # posts=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found error")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"post with id:{id} not found error"
    return {"data" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):

    cursor.execute("""DELETE FROM posts WHERE id =%s returning *""",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content =%s,published=%s WHERE id =%s RETURNING *""",(post.title,post.content,post.published, str(id)))

    updated_post=cursor.fetchone()
    conn.commit()
   
     
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
     
    return {"message" : updated_post}
