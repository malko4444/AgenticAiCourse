from sqlalchemy import create_engine #use to make the conection with the data base 
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

data_base_url = os.getenv('DATA_BASE_URI')
print(data_base_url,"the url of from the env dile ")
engine = create_engine(data_base_url) #create the connection with the data base
sessionlocal = sessionmaker( autocommit= False,autoflush=False, bind=engine)  #create a session to interact with the database

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
