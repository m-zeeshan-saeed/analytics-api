from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, database,models
from sqlalchemy.orm import Session, joinedload
from blogs.router import oauth




router = APIRouter(tags=["Blogs"],prefix="/blog")
get_db = database.get_db



@router.get("/", status_code=status.HTTP_207_MULTI_STATUS,response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog





@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show(id: int, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
    blog = db.query(models.Blog).options(joinedload(models.Blog.creator)).filter(models.Blog.id == id).first()
    if not blog:
        details = f"Blog with the id {id} is not available"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=details)

    return blog

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int,db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.update(request.dict(),synchronize_session=False)
    db.commit()
    return "Updated"
