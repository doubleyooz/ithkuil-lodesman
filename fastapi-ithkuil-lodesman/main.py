from app.translations import routes as translation_routes
from app.auth import routes as auth_routes
from app.users import routes as user_routes
from fastapi import FastAPI

app = FastAPI()
app.include_router(translation_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
