from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# @function_tool
# def get_weather(city: str) -> str:
#     return f"The weather in {city} is sunny"
@function_tool
def fetch_weather(location: str) -> str:
    """
   goal: Fetches the current weather for a given location.
   arguments:
    - location (str): The name of the location to fetch the weather for.
    Expected OutPut:
    - A string describing the current weather conditions in the specified location.
    """
    # Simulate fetching weather data
    print(f"Fetching weather for {location}...")
    return f"The current weather in {location}  is sunny with a temperature of 25°C."
agent = Agent(
    name="Assistant",
    instructions="You are a weather assistant..",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    # tools=[get_weather]
)

query = input("Enter the query: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)