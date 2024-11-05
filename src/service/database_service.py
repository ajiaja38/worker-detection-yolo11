import os
import pymongo
from datetime import datetime, timedelta
from uuid import uuid4

from dotenv import load_dotenv
import pymongo.database
load_dotenv()

MONGO_URI: str = os.getenv("MONGO_DEV")

client: pymongo.MongoClient = pymongo.MongoClient(MONGO_URI)
db: pymongo.database = client["hidroponik-sg"]
collection = db["reports"]


def save_to_database(output_name: str) -> None:
  try:
    guid = f"Reports-{uuid4()}-2024"
    date: datetime = datetime.now() - timedelta(hours=7)
    
    report_data = {
      "guid": guid,
      "reportContent": "Detection Object TNWK",
      "reporterGuid": "-",
      "reporterName": "-",
      "imageurl": output_name,
      "latitude": -4.92735132216021,
      "longitude": 105.77693902350316,
      "reportType": "Output AI",
      "date": date,
      "createdAt": date,
    }
    
    result = collection.insert_one(report_data)
    print(f"Saved to database: {result.inserted_id}")
    
  except Exception as e:
    print(f"Failed to save to database: {e}")
    raise