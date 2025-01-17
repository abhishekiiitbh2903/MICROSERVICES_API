from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int
    rating:Optional[int]=None

    class Config:
        extra="forbid"

        
app = FastAPI()

my_posts=[
    {"title": "title of post 1", "content": "content of post 1", "id": 1,"published": True,"rating": 4},
    {"title": "title of post 2", "content": "content of post 2", "id": 2,"published": False,"rating": 3},
    {"title": "title of post 3", "content": "content of post 3", "id": 3,"published": True,"rating": 5}
    ]

#! Function to find the post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

#! Starting point of the API
@app.get("/")
async def root():
    return {"message": "Hey! Writing production Grade Server in FastAPI"}

#! To create a new post
@app.post("/create_post",status_code=201) #!Changing  Default status code from 200 to 201 [New entry created]
async def create_post(payload: Post):
    my_posts.append(payload)
    return {"post": payload}

#! To get the latest post
@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    if len(post) == 0:
        raise HTTPException(status_code=404, detail="Post not found[No Post]")
    return {"post": post}

#! To get a specific post
@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}


#! To delete a specific post
@app.delete("/posts/{id}",status_code=204)
async def delete_post(id: int):
    post = find_post(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        my_posts.remove(post)
    except ValueError:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    #! Standard Practice: When we delete something then we should not send any response back to the user



#! Get all the Posts
@app.get("/posts")
async def get_posts():
    return {"posts": my_posts}