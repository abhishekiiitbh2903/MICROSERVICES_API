from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_post")
async def create_post(payload: dict = Body(...)):
    return {"post": payload}