from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user, get_db
from app.schemas.task import TaskResponse, TaskCreate
from app.models.user import User
from app.models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskResponse])
def get_task(current_user: User = Depends(get_current_user), 
            db: Session = Depends(get_db),
            limit: int = Query(default=80, ge=1, le=100),
            offset: int = Query(default=0, ge=0)):
    
    tasks = db.query(Task).filter(Task.user_id == current_user.id
            ).order_by(Task.is_completed.asc(), Task.created_at.desc()
            ).offset(offset).limit(limit).all()

    return tasks

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="No se pudo crear la tarea")
    
    return new_task
