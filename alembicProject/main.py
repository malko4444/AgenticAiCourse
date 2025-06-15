from fastapi import FastAPI
from routes import todo_routes, user_routes
# from routes.user_routes import user_router
from dotenv import load_dotenv
load_dotenv()

from typing import List
import uvicorn
from typing import Optional

app = FastAPI()
app.include_router(todo_routes.todo_router, prefix="/todos", tags=["Todos"])
app.include_router(user_routes.user_router, prefix="/users", tags=["Users"])


@app.get("/" )
def read_root():
    return {"message": "Welcome to the Todo API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
