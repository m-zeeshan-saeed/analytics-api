from typing import Union

from fastapi import FastAPI, Depends, status, Response, HTTPException
from api.events import router as event_router
from blogs.database import engine, SessionLocal
from blogs import models
from blogs import schemas,models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(event_router, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Main": "Main Page"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health")
def read_api_health():
    return {"Testing": "API"}


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Method

@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Retrieve Data

@app.get("/blog", status_code=status.HTTP_207_MULTI_STATUS)
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
async def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        details = f"Blog with the id {id} is not available"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=details)
        # Response Method

        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"Details":f"Blog with the id {id} is not available"}


    return blog

# Delete Data


@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


# Update Data

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.update(request.dict(),synchronize_session=False)
    db.commit()
    return "Updated"
