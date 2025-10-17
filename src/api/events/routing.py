from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema

router = APIRouter()


@router.get("/")
def read_events():
    return{
        "items":[1,2,3,4,5]
    }


@router.get("/{event_id}")
def get_events(event_id:int) -> EventSchema :
    return{
        "id": event_id
    }


@router.get("/")
def read_events()-> EventListSchema:
    return{
        "results":[{"id":1},{"id":2},{"id":3},{"id":4}]
    }
