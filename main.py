from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_post")
async def create_post(payload: dict = Body(...)): 
# Fetching body from request object and converting it to dictionary and assigning it to payload
    return {"post": payload}


@app.post("/create_post")
async def create_post(payload: dict = Body(...)): 
    # Fetching body from request object and converting it to dictionary and assigning it to payload
    return {f"title : {payload['title']} content : {payload['content']}"}