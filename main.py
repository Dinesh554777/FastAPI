from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
app=FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating : Optional[int] = None
    

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/posts")
async def get_posts():
    return {"message": "Here are the posts."}

@app.post("/create_posts")
async def create_post(post: Post):
    
    print(post.dict())
    
    return {"data":post}
