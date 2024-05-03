from fastapi import APIRouter, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .. import schemas, hashing, jwt_auth, models

from ..database import get_db


router = APIRouter(prefix="/users", tags=['User'])






# Create user
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session= Depends(get_db)):
        hashed_password = hashing.hash_password(user.password)
        users = models.Users(name= user.name, username=user.username, email=user.email, password=hashed_password)
        db.add(users)
        db.commit()
        db.refresh(users)

        return {"message": "User created successfully"}



# Deleting user
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session= Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"cordinate with id: {id} was not found")

    user_query.delete(synchronize_session=False)
    db.delete(user)
    db.commit()
    return f'The user  is deleted'



