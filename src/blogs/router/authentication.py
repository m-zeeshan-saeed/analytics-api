from fastapi import APIRouter, Depends, status, HTTPException
from blogs import schemas, database, models
from sqlalchemy.orm import Session
from blogs.hashing import Hash

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
async def login(request: schemas.Login, db:Session = Depends(database.get_db)):
    user =  db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials {user}")

    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect Password")

    return {
        "message": "Login successful",
        "user": {
            "username": user.username,
            "email": user.email
        }
    }
