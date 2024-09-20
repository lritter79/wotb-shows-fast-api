from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from bson import ObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from dal import ShowDAL
from models import Show

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

COLLECTION_NAME = "wotb_shows"
MONGODB_URI = os.getenv("MONGODB_URI")
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    print("Connecting to MongoDB...")   
    print(MONGODB_URI)
    client = AsyncIOMotorClient(MONGODB_URI)

    database = client.get_default_database()

    # Ensure the database is available:
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    shows = database.get_collection(COLLECTION_NAME)
    app.show_dal = ShowDAL(shows)

    # Yield back to FastAPI Application:
    yield

    # Shutdown:
    client.close()

app = FastAPI(lifespan=lifespan, debug=DEBUG)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shows")
async def read_shows() -> list[Show]:
    return [i async for i in app.show_dal.list_shows()]

@app.get("/shows/{show_id}")
async def read_show(show_id: str) -> Show:
    return await app.show_dal.get_show(show_id)

class NewShowResponse(BaseModel):
    id: str

@app.post("/shows")
async def create_show(show: Show) -> NewShowResponse:
    return {"show": show.model_dump()}

@app.put("/shows/{show_id}")
async def update_show(show_id: str, show: Show) -> bool:
    return await app.show_dal.update_show(show_id, show)

@app.delete("/shows/{show_id}")
async def delete_show(show_id: str) -> bool:
    return await app.show_dal.delete_show(show_id)

class DummyResponse(BaseModel):
    id: str
    when: datetime

@app.get("/api/dummy")
async def get_dummy() -> DummyResponse:
    return DummyResponse(
        id=str(ObjectId()),
        when=datetime.now(),
    )


def main(argv=sys.argv[1:]):
    try:
        pass
        #uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
    
# # @app.get("/items/{item_id}")
# # async def read_item(item_id: int):
# #     return {"item_id": item_id}

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}

# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
#     user_id: int,  
#     q: Annotated[Union[str, None], Query(title="Query string",             
#                                                         description="Query string for the items to search in the database that have a good match",max_length=50)] = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item