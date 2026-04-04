from fastapi import FastAPI
from app.routers import auth, users, tasks
from app.models import User, Task

app = FastAPI(title="TaskFlow API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "TaskFlow api funcionando"}
