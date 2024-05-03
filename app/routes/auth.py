from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, hashing, jwt_auth
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
                    tags=['Aunthentication'],
                    
    )

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not hashing.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = jwt_auth.create_access_token(data={"user_id": user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}