from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Tavily client
tavily_client = TavilyClient(api_key="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")

# Gemini/OpenAI setup
gemini_api_key = os.getenv("GOOGLE_API_KEY")
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define Google search tool using Tavily
@function_tool
def google_search(query: str) -> str:
    """
    goal: Search the internet for a given query using Tavily and return the top result.
    arguments:
    - query (str): The user's question or topic to search.
    Expected Output:
    - A string containing a summary or answer from the search result.
    """
    print(f"Searching Google for: {query}")
    result = tavily_client.search(query=query, search_depth="basic", include_answer=True)
    return result.get("answer", "No relevant information found.")

# Define agent with the google search tool
agent = Agent(
    name="Search Assistant",
    instructions="You are a helpful AI that answers user questions by searching the internet.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[google_search]
)

# Run agent with user query
query = input("Enter your search query: ")

result = Runner.run_sync(agent, query)

print("🔍 Answer:", result.final_output)
 