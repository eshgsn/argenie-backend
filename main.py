import string

from fastapi import FastAPI, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can specify specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["project1"]
collection = db["argenie"]



class DemoModel(BaseModel):
    movie :str
    title :str
    genres :str
    year :str
    Rating :str
    RottenTomato :str



@app.post("/demo/")
async def create_demo(demo: DemoModel):
    demo_dict = demo.dict()
    try:
        result = await collection.insert_one(demo_dict)
        demo_dict["_id"] = str(result.inserted_id)
        return demo_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/demo/")
async def read_demo(page: int = Query(1, gt=0), per_page: int = Query(10, gt=0)):
    skip_count = (page - 1) * per_page
    users = []
    async for user in collection.find({}).skip(skip_count).limit(per_page):
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users.append(user)
    return users



@app.put("/demo/{_id}")
async def update_demo(_id: str, demo: DemoModel):
    demo_dict = demo.dict()
    print("value of demo_id is ", _id)
    await collection.update_one({"_id": ObjectId(_id)}, {"$set": demo_dict})
    print("value of demo_id is 2 ", _id)
    updated_demo = await collection.find_one({"_id": ObjectId(_id)})
    if updated_demo:
        return updated_demo
    raise HTTPException(status_code=404, detail="Demo not found")



@app.delete("/demo/{_id}")
async def delete_demo(_id: str):
    print(_id)
    obj_id = ObjectId(_id)
    res = await collection.delete_one({"_id": obj_id})
    return res
    
