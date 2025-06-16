from fastapi import APIRouter, HTTPException, Depends
from config.database import get_db
from models.todo_model import Todos
from validations.validation import TodoCreate
from sqlalchemy.orm import Session
from utils.utils_helper_function import verify_token

todo_router = APIRouter()


@todo_router.post("/create/")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), user= Depends(verify_token)): 
    try:
        print("the verifief token ",user)
        db_todo = Todos(user_id=user["user_id"],title=todo.title, description=todo.description, completed=todo.completed, status=todo.status)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
            "message": "Todo created successfully",
            "data": db_todo,
            "currentLoggedInUser":user,
            "status": "success"
        }
    except Exception as e:
        print(f"Error creating todo: {str(e)}")
        return{
            "error": "Error creating todo",
            "details": str(e)

        }
        



@todo_router.delete("/deletetodos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(todo)
        db.commit()
        return {
            "message": "Todo deleted successfully",
            "status": "success"
            
        }
    except Exception as e:
        return{
            "error": "Error deleting todo",
            "details": str(e)
        }
@todo_router.put("/update/{updateid}")
def update_todo(updateid:int ,todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        todo_to_update = db.query(Todos).filter(Todos.id == updateid).first()
        if not todo_to_update:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_to_update.title = todo.title
        todo_to_update.description = todo.description
        todo_to_update.completed = todo.completed
        todo_to_update.status = todo.status

        db.commit()
        db.refresh(todo_to_update)
        return todo_to_update
    except Exception as e:
        return {
            "error": "Error updating todo",
            "details": str(e)
        }
@todo_router.get("/")
def read_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todos).all()
        return{
            "data": todos,
            "status":"success",
            "message": "Todos retrieved successfully"

        }
    except Exception as e:
        return {
            "error": "Error retrieving todos",
            "details": str(e)
        }
