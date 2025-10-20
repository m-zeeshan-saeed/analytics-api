from typing import Union

from fastapi import FastAPI
from api.events import router as event_router
from blogs.blog import router as blog_router


app = FastAPI()
app.include_router(event_router, prefix="/api/events")
app.include_router(blog_router, prefix="/blogs")


@app.get("/")
def read_root():
    return {"Main": "Main Page"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health")
def read_api_health():
    return {"Testing": "API"}
