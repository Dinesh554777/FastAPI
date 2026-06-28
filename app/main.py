from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    
    new_post=cursor.fetchone()
    conn.commit()

    
    return {"data":new_post}

@app.get("/posts/{id}")
def get_one_post(id : int,):
    cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id)))
    posts=cursor.fetchone()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found error")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"post with id:{id} not found error"
    return {"data" : posts}

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
