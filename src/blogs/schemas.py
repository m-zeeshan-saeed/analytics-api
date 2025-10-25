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




class show_user(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []

    model_config = {"from_attributes": True}

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: Optional[show_user] = None

    model_config = {"from_attributes": True}

class Login(BaseModel):
    username: str
    password: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
