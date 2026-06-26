from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating : Optional[int] = None
    

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

my_posts=[{"title": "My posts", "content":"My posts content", "id": 3}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/posts")
async def get_posts():
    return {"message": my_posts}

@app.get("/posts/{id}")
def get_one_post(id : int):
    post = find_posts(id)
    return {"data" : post}

@app.post("/posts")
async def create_post(post: Post):

    post_dict=post.dict()
    post_dict['id'] = randrange(1,10000000)
    my_posts.append(post_dict)
    
    return {"data":post_dict}
