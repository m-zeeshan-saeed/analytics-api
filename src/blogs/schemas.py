from typing import List, Optional
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):

    model_config = {"from_attributes": True}



class User(BaseModel):
    username: str
    email: str
    password: str

    model_config = {"from_attributes": True}


class show_user(BaseModel):
    username: str
    email: str
    blogs: List[Blog]

    model_config = {"from_attributes": True}

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: show_user

    model_config = {"from_attributes": True}

class Login(BaseModel):
    username: str
    password: str

    model_config = {"from_attributes": True}
