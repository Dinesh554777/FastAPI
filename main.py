from fastapi import FastAPI
from fastapi.params import Body
app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/posts")
async def get_posts():
    return {"message": "Here are the posts."}

@app.post("/create_posts")
async def create_post(payload: dict=Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']}  content: {payload['content']}" }