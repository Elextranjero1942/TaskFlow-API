from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }

@router.patch("/me", response_model=UserUpdate)
def update_profile(user_update: UserUpdate, 
                current_user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    data = user_update.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, detail="No enviaste datos")
    
    changes = any(
        getattr(current_user, field) != value
        for field, value in data.items()
    )

    if not changes:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    new_email = data.get("email")
    if new_email and new_email != current_user.email:
        existing_user = db.query(User).filter(User.email == new_email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    for field, value in data.items():
        setattr(current_user, field, value)

    try:
        db.commit()
        db.refresh(current_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo actualizar el perfil")

    return {
        "name": current_user.name,
        "email": current_user.email
    }


    