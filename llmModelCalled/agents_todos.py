from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
MONGO_URI = "mongodb+srv://zubair:zubair@cluster0.gxseg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["todos"]
collection = db["agentic_ai"]

# OpenAI setup
gemini_api_key = os.getenv("GOOGLE_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Tool 1: Add Todo
@function_tool
def add_todo(title: str, description: str, is_completed: bool = False) -> str:
    """
    Adds a new todo to the MongoDB collection.
    Parameters:
    - title (str): The title of the todo.
    - description (str): The description of the todo.
    - is_completed (bool): The completion status of the todo (default is False).
    Returns a success message upon adding the todo.
    If a todo with the same title already exists, it will be overwritten.

    """
    todo = {"title": title, "description": description, "is_completed": is_completed}
    collection.insert_one(todo)
    return f"Todo '{title}' added successfully."

# Tool 2: Update Todo by title
@function_tool
def update_todo(title: str, new_description: str = None, is_completed: bool = None) -> str:
    """
    Updates a todo by its title.
    Allows updating the description and completion status.
    If no updates are provided, the todo remains unchanged.
    If the todo with the given title does not exist, returns a message indicating that.
    """
    update_fields = {}
    if new_description:
        update_fields["description"] = new_description
    if is_completed is not None:
        update_fields["is_completed"] = is_completed

    result = collection.update_one({"title": title}, {"$set": update_fields})
    if result.matched_count:
        return f"Todo '{title}' updated successfully."
    else:
        return f"No todo found with title '{title}'."
@function_tool
def get_todos() -> str:
    """
    Retrieves all todos from the MongoDB collection.
    Returns a formatted string of all todos.
    If no todos are found, returns a message indicating that.

    """
    todos = list(collection.find())
    if not todos:
        return "No todos found."
    
    todo_list = "\n".join([f"{todo['title']}: {todo['description']} (Completed: {todo['is_completed']})" for todo in todos])
    return f"Todos:\n{todo_list}"
# Tool 3: Delete Todo by title
@function_tool
def delete_todo(title: str) -> str:
    """
    Deletes a todo from the MongoDB collection by its title.
    """
    result = collection.delete_one({"title": title})
    if result.deleted_count:
        return f"Todo '{title}' deleted successfully."
    else:
        return f"No todo found with title '{title}'."

# Setup Agent
agent = Agent(
    name="Todo Assistant",
    instructions="You manage a todo list and respond to user's natural language requests using available tools.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[add_todo, update_todo, delete_todo, get_todos]
)

# Ask user
query = input("Enter your query: ")

# Run agent
result = Runner.run_sync(
    agent,
    query
    )

# Output
print(result.final_output)
