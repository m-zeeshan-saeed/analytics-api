from typing import Union, List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from api.events import router as event_router
from blogs.database import engine, SessionLocal
from blogs import models
from blogs import schemas,models
from sqlalchemy.orm import Session
from blogs.hashing import Hash

models.Base.metadata.create_all(bind=engine)


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

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(**request.dict(),user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Retrieve Data

@app.get("/blog", status_code=status.HTTP_207_MULTI_STATUS,response_model=List[schemas.ShowBlog], tags=["Blogs"])
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["Blogs"])
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


@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
async def delete_blog(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


# Update Data

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    blog.update(request.dict(),synchronize_session=False)
    db.commit()
    return "Updated"



@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.show_user, tags=["Users"])
async def create_users(request: schemas.User,db: Session =Depends(get_db)):
    hashedPassword = await Hash.bcrypt(request.password)
    new_user = models.User(**request.dict(exclude={"password"}),password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", status_code=status.HTTP_207_MULTI_STATUS,response_model=schemas.show_user, tags=["Users"])
async def showUser(id: int ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This user {id} is not in our database")
    return user
