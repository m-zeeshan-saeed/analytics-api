from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, database,models
from sqlalchemy.orm import Session
from blogs.hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=["Users"])
get_db = database.get_db




@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.show_user)
def create_users(request: schemas.User,db: Session =Depends(get_db)):
    hashedPassword =  Hash.bcrypt(request.password)
    user_data = request.dict()
    user_data["password"] = hashedPassword

    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_207_MULTI_STATUS,response_model=schemas.show_user)
def showUser(id: int ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This user {id} is not in our database")
    return user
