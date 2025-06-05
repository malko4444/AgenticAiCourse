from sqlalchemy import create_engine #use to make the conection with the data base 
from sqlalchemy.orm import sessionmaker


data_base_url = "postgresql://neondb_owner:npg_VQq5XoinZxO6@ep-bold-glade-a8pjeve3-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"  #postgreSQL database file
engine = create_engine(data_base_url) #create the connection with the data base
sessionlocal = sessionmaker( autocommit= False,autoflush=False, bind=engine)  #create a session to interact with the database