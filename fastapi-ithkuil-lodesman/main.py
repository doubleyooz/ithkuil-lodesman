from app.translations import controller as translations_controller
from app.auth import controller as auth_controller
from app.users import controller as users_controller
from fastapi import FastAPI

app = FastAPI()
app.include_router(translations_controller.router)
app.include_router(auth_controller.router)
app.include_router(users_controller.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
