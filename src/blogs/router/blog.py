from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, database,models
from sqlalchemy.orm import Session


router = APIRouter(tags=["Blogs"],prefix="/blog")
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(**request.dict(),user_id = request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.get("/", status_code=status.HTTP_207_MULTI_STATUS,response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        details = f"Blog with the id {id} is not available"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=details)
        # Response Method

        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"Details":f"Blog with the id {id} is not available"}


    return blog

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.update(request.dict(),synchronize_session=False)
    db.commit()
    return "Updated"
