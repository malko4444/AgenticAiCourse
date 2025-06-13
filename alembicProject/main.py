from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import Session
from config.database import sessionlocal, engine
from models.todo_model import Todos, Base,Users
from pydantic import BaseModel
from typing import List
import uvicorn
from typing import Optional

Todos.metadata.create_all(bind=engine)  # Create the tables in the database same work as alembic do dont 
app = FastAPI()
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    status: Optional[str] = None


class TodoResponse(TodoCreate):
    id: int
    user: UserResponse  # ✅ Include nested user here

    class Config:
        orm_mode = True


@app.post("/createuser/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print("Creating user:", user)
        db_user = Users(name=user.name, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/deletetodos/{todo_id}", response_model=TodoResponse)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(todo)
        db.commit()
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.put("/updatetodo/{updateid}",response_model=TodoResponse)
def update_todo(updateid:int ,todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        todo_to_update = db.query(Todo).filter(Todo.id == updateid).first()
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
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.post("/createtodos/{id}")
def create_todo( id, todo: TodoCreate, db: Session = Depends(get_db)): 
    try:
        db_todo = Todos(user_id=id,title=todo.title, description=todo.description, completed=todo.completed, status=todo.status)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todos).all()
    return todos


@app.get("/" )
def read_root():
    return {"message": "Welcome to the Todo API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
 