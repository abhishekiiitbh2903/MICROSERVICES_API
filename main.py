from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, model_validator
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int
    rating:Optional[int]=None

    class Config:
        extra="forbid"

class update_Post(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None
    id: Optional[int] = None

    class Config:
        extra = "forbid"

    @model_validator(mode="before")
    def at_least_one_field_required(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided in the request.")
        return values
        
app = FastAPI()

my_posts=[
    {"title": "title of post 1", "content": "content of post 1", "id": 1,"published": True,"rating": 4},
    {"title": "title of post 2", "content": "content of post 2", "id": 2,"published": False,"rating": 3},
    {"title": "title of post 3", "content": "content of post 3", "id": 3,"published": True,"rating": 5}
    ]

#! Function to find the post
def find_post(post_id: int):
    return next((post for post in my_posts if post["id"] == post_id), None)
        

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


'''
For Updating the post we have two ways:
1. Put Method: Update the entire post [Requires entire Body to process the request]
2. Patch Method: Update the part of the post [Requires the field that needs to be updated only]
'''

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    post_to_update = find_post(id)
    if post_to_update is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post_to_update.update(post.model_dump())
    return {"post": post_to_update}

'''
Doing the same with patch method
'''

@app.patch("/posts/{id}")
async def update_post(id: int, post: update_Post):
    post_to_update = find_post(id)
    if post_to_update is None:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = post.model_dump(exclude_unset=True)  
    post_to_update.update(update_data)  
    return {"post": post_to_update}


#! Get all the Posts
@app.get("/posts")
async def get_posts():
    return {"posts": my_posts}