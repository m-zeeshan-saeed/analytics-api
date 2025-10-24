from typing import Union

from fastapi import FastAPI
from blogs.database import engine
from blogs import models
from blogs.router import blog
from blogs.router import user
from blogs.router import authentication


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)


@app.get("/")
def read_root():
    return {"Main": "Main Page"}
