from fastapi import FastAPI,APIRouter,HTTPException 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi import File,UploadFile, Form
# marke the static folder to access the file that the server want to access to the frontend 
from fastapi.staticfiles import StaticFiles
#  shutil build in library to save the file or to move the file from one folfer to another 
import shutil#creat the new file 
import os#maintain the path of the file

from pydantic import BaseModel
from typing import Optional
import uvicorn
UPLOAD_Folder = "upload"
os.makedirs(UPLOAD_Folder, exist_ok=True)

app = FastAPI()
# to tell the fast api that dont call the validation error by default function which is called RequestValidationError
# and call the custom function that we created below 

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(map(str, error["loc"])),
            "message": error["msg"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "errors": errors,
        },
    )

app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.post("/uploadfileWithValidation")
async def create_upload_file_with_validation(
    file: UploadFile = File(...),
    ):
    try:
        # the two lines save the file to the path that we are created using the shuttle library 
        with open(os.path.join(UPLOAD_Folder, file.filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_url = f"/file/{file.filename}"    
        return {"filename": file.filename,"file_url": file_url}
    except Exception as e:
        return {
            "message" : "error",
            "statue" : "error",
            "error" : str(e)
         }  
class person(BaseModel):
    name: str
    age: int
    email: str
    
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
@app.post("/items/{item_id}")
async def findItem(item_id: int, item: Item , q: str, person: person):
    try:
        # Simulate some processing
        if item_id > 10:
            raise HTTPException(status_code=400, detail="Item ID should be less than or equal to 10")
        return{"item_id": item_id}
    except Exception as e:
        return {
            "message": "error",
            "statue": "error",
            "error": str(e)
        }      
app.mount("/file",StaticFiles(directory=UPLOAD_Folder), name="file")
# @app.post("/uploadfile")
# async def create_upload_file(file: UploadFile = File(...)):
#     try:
#         # the two lines save the file to the path that we are created using the shuttle library 
#         with open(os.path.join(UPLOAD_Folder, file.filename), "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         file_url = f"/file/{file.filename}"    
#         return {"filename": file.filename,"file_url": file_url}
#     except Exception as e:
#         return {
#             "message" : "error",
#             "statue" : "error",
#             "error" : str(e)
#          }
# userApp = APIRouter()

# @userApp.get("/user/{user_id}/{name}")
# def read_root(user_id, name:Optional[str] = None):
#     try:
#         # Simulate some processing
#         return{
#             "message" :"succes you are in the root path the",
#             "status" :"success",
#             "user_id" : user_id,
#             "name" : name 
#         }
#     except Exception as e:
#         return {
#             "message" : "error",
#             "statue" : "error",
#             "error" : str(e)
#         }


# @userApp.get("/queryCheck")
# def read_root(id:int,q:str,  name:Optional[str] = None ): 
#     try:
#         # Simulate some processing
#         if id >10:
#             raise ValueError("id should be less than 10")


#         return{

#             "message" :"succes you are in the root path the",
#             "status" :"success",
#             "user_id" : q,
#             "name" : name 
#         }
#     except Exception as e:
#         return {
#             "message" : "error",
#             "statue" : "error",
#             "error" : str(e)
#         }

# @userApp.get("/bodyCheck")
# def read_root(person: person):
#     try:
#         # Simulate some processing
#         return{

#             "message" :"succes you are in the root path the",
#             "status" :"success",
#             "user_id" : person.age,
#             "name" : person.name,
#             "email" : person.email
            
#         }
#     except Exception as e:
#         return {
#             "message" : "error",
#             "statue" : "error",
#             "error" : str(e)
#         }

# app.include_router(userApp,prefix="/user", tags=["user"])


    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
 