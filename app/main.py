from fastapi import FastAPI
from app.routers import auth, users
from app.models import User, Task

app = FastAPI(title="TaskFlow API")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "TaskFlow api funcionando"}
