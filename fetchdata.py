import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from io import StringIO  # Required for Python 3

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["project1"]
collection = db["argenie"]


csv_url = "https://raw.githubusercontent.com/kromerm/adfdataflowdocs/master/sampledata/moviesDB.csv"

df = pd.read_csv(csv_url)

data = df.to_dict(orient="records")

collection.insert_many(data)

print("Data inserted into MongoDB successfully!")