from typing import List,Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode: True



class User(BaseModel):
    username: str
    email: str
    password: str
    class Config():
        orm_mode: True


class show_user(BaseModel):
    username: str
    email: str
    blogs: List[Blog]= []

    class Config():
        orm_mode: True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: Optional[show_user] = None
    class Config():
        orm_mode: True
