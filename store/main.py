from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


class Store(BaseModel):
    name: str
    location: List[str]
    profits: str


stores = [
    {
        "id": 1,
        "name": "Store 1",
        "location": ["11.4", "1.3"],
        "profits": "4% up"
    },
    {
        "id": 2,
        "name": "Store 2",
        "location": ["1.4", "445"],
        "profits": "3% down"
    }
]


app = FastAPI()


@app.get("/stores/")
def get_stores():
    return stores


@app.get("/stores/{id}")
def get_store(id: int):
    for store in stores:
        if store["id"] == id:
            return store
    return {}


@app.post("/stores/")
def create_store(store: Store):
    last_store = stores[-1]
    new_store_id = last_store["id"] + 1 if last_store else 0
    stores.append({
        "id": new_store_id,
        "name": store.name,
        "location": store.location,
        "profits": store.profits
    })
    return store


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
