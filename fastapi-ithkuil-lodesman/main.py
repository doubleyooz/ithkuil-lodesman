from typing import Union
from translations import routes
from fastapi import FastAPI

app = FastAPI()
app.include_router(routes)

@app.get("/")
def read_root():
    return {"Hello": "World"}