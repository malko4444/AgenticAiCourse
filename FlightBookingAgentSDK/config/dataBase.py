import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
def connect_db():
    try:
        client = MongoClient(os.getenv("DB_URI"))
        print("Connected to the database successfully")
        return client
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
dataBase_client = connect_db()
db = dataBase_client["FlightBookingAgentSDK"]
