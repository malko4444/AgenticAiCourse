from fastapi import FastAPI
from pymongo import MongoClient
import uvicorn
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel



load_dotenv()



app = FastAPI()
class Todo(BaseModel):
    title: str
    description: str
    status: bool

# DB_URI is available in .env file 
# print(os.getenv("DB_URI"))
def connect_db():
    try:
        client = MongoClient(os.getenv("DB_URI"))
        print("Connected to the database successfully")
        return client
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

client = connect_db()
db = client["fastapidb"]

# print(client)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/todos")
def fetch_all_toDos():
    try:
        todos = db.todos.find()
        listTodos = []
        for todo in todos:
            todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
            listTodos.append(todo)
        return {
            "message": "success",
            "status": "success",
            "data": listTodos
        }
    except Exception as e:
        return {
            "message": "error",
            "status": "error",
            "error": str(e),
            "data": []
        }
        
        
@app.get("/todos/{todo_id}")
def fetch_todo(todo_id: str):
    try:
        print("the user id ",todo_id)
        todo = db.todos.find_one({"_id":ObjectId(todo_id)})
        print("the todo is ",todo)
        if todo:
            todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
            return {
                "message": "success",
                "status": "success",
                "data": todo
            }
        else:
            return {
                "message": "Todo not found",
                "status": "error",
                "data": {}
            }
    except Exception as e:
        return {
            "message": "error",
            "status": "error",
            "error": str(e),
            "data": {}
        }   

@app.post("/create_todos")
def create_todo(todo: Todo):
    try:
        todo = {
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": str(datetime.now())
        }
        result = db.todos.insert_one(todo)
        todo["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        return {
            "message": "Todo created successfully",
            "status": "success",
            "data": todo
        }
    except Exception as e:
        return {
            "message": "error",
            "status": "error",
            "error": str(e),
            "data": {}
        }
    
@app.delete("/delete_todo/{todo_id}")
def delete_todo(todo_id: str):
    try:
        result = db.todos.delete_one({"_id": ObjectId(todo_id)})
        if result.deleted_count > 0:
            return {
                "message": "Todo deleted successfully",
                "status": "success",
                "data": {}
            }
        else:
            return {
                "message": "Todo not found",
                "status": "error",
                "data": {}
            }
    except Exception as e:
        return {
            "message": "error",
            "status": "error",
            "error": str(e),
            "data": {}
        }
@app.put("/update_todo/{todo_id}")
def update_todo(todo_id: str, todo: Todo):
    try:
        updated_todo = {
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "updated_at": str(datetime.now())
        }
        result = db.todos.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_todo})
        if result.modified_count > 0:
            updated_todo["_id"] = todo_id  # Add the ID to the updated todo
            return {
                "message": "Todo updated successfully",
                "status": "success",
                "data": updated_todo
            }
        else:
            return {
                "message": "Todo not found or no changes made",
                "status": "error",
                "data": {}
            }
    except Exception as e:
        return {
            "message": "error",
            "status": "error",
            "error": str(e),
            "data": {}
        }        
if __name__ == "__main__":
    uvicorn.run("main1:app", host="127.0.0.1", port=8000, reload=True)
 