import asyncio
import os
import random
import uuid
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from config.dataBase import db
from routes import auth_routes

from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
    OpenAIChatCompletionsModel,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pymongo import MongoClient
# Load environment variables
gemini_api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

### CONTEXT
class AirlineAgentContext(BaseModel):
    passenger_name: str | None = None
    confirmation_number: str | None = None
    seat_number: str | None = None
    flight_number: str | None = None

### TOOLS
# change this tool to the simple flight booking tool and stored the data in the mongo db database


@function_tool
async def simple_flight_booking(
    passenger_name: str,
    seat_number: int ,
    passport_number: int
):
    """ A simple flight booking tool that checks if a seat is available and books it.
    :param passenger_name: Full name of the passenger
    :param seat_number: Seat number to book (1-120) 
    :param passport_number: Passport number of the passenger
    :return: A message indicating success or failure of the booking
    """
    # seat number must be less than 120
    if seat_number < 1 or seat_number > 120:
        return {"error": "Invalid seat number. Must be between 1 and 120."}
    # Check if a record with the same passport number already exists
    existing_booking = db.bookings.find_one({"passport_number": passport_number})
    existing_seat = db.bookings.find_one({"seat_number": seat_number})
    if existing_seat:
        existing_seat["_id"] = str(existing_seat["_id"])
        return {
            "error": f"Seat {seat_number} is already booked by {existing_seat['passenger_name']}."
        }

    if existing_booking:
        # Convert ObjectId to string or remove it
        existing_booking["_id"] = str(existing_booking["_id"])
        return {
            "message": f"Flight already booked for {existing_booking['passenger_name']} on {existing_booking['passport_number']}.",
            # "booking_info": existing_booking
        }

    #qw If no existing booking, insert new booking
    booking_info = {
        "passenger_name": passenger_name,
        # "airline_name": airline_name,
        "seat_number": seat_number,
        "passport_number": passport_number,
    }

    result = db.bookings.insert_one(booking_info)

    # Add the ObjectId as a string to the response
    booking_info["_id"] = str(result.inserted_id)

    return {
        "message": f"Flight booked successfully for {passenger_name}.",
        "booking_info": booking_info
    }

@function_tool(name_override="faq_lookup_tool", description_override="Lookup frequently asked questions.")
async def faq_lookup_tool(question: str) -> str:
    if "bag" in question or "baggage" in question:
        return "One bag allowed (max 50 lbs, 22x14x9 in)."
    elif "seats" in question:
        return "120 seats total: 22 business, 98 economy. Exit rows: 4, 16."
    elif "wifi" in question:
        return "Free WiFi available. Connect to Airline-Wifi."
    return "Sorry, I don't know the answer to that question."

### AGENTS

faq_agent = Agent[AirlineAgentContext](
    name="FAQ Agent",
    handoff_description="An agent for answering airline FAQs.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a FAQ agent. If a customer asks a common question, use the FAQ tool.""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[faq_lookup_tool],
)
booking_agent = Agent[AirlineAgentContext](
    name="Flight Booking Agent",
    handoff_description="An agent that books a flight seat.",
   instructions = f"""{RECOMMENDED_PROMPT_PREFIX}
You are a flight booking agent for an airline.

Your task is to help users book their flights by collecting the following details:
- Full Name
- Seat Number
- Passport Number

You will use the `simple_flight_booking` tool to confirm the booking.

When the user provides their full name, seat number, and passport number.


Always try to extract this information from the user’s input, even if it's in natural or unstructured language.

Once you have all four required pieces of information, call the `simple_flight_booking` tool immediately to confirm the booking.

If any information is missing, ask *only* for the missing details — do not repeat or ask again for already known values.
"""
,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[simple_flight_booking],
)
triage_agent = Agent[AirlineAgentContext](
    name="Triage Agent",
    handoff_description="Routes requests to FAQ or Booking agent.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a smart triage agent for an airline assistant.

When the user input clearly matches either a booking intent or a question, you must immediately and automatically hand off to the appropriate agent.

Do NOT ask the user if they want a handoff — just route them to the correct agent.
Use the FAQ agent for common questions.
Use the Flight Booking agent when the user provides booking info like name, seat number, or confirmation number.
""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[
        faq_agent,
        handoff(agent=booking_agent),
    ],
)

# Connect agents
faq_agent.handoffs.append(triage_agent)
booking_agent.handoffs.append(triage_agent)

### FASTAPI SETUP

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_context = AirlineAgentContext()
conversation_id = uuid.uuid4().hex[:16]
input_items: list[TResponseInputItem] = []
current_agent: Agent[AirlineAgentContext] = triage_agent

@app.post("/chat")
async def chat_with_agent(request: Request):
    global input_items, current_agent

    user_input = await request.body()
    print(f"Received user input: {user_input}")
    user_input = user_input.decode("utf-8").strip()

    if not user_input:
        return {"error": "Empty message."}

    with trace("Customer service", group_id=conversation_id):
        input_items.append({"content": user_input, "role": "user"})
        result = await Runner.run(current_agent, input_items, context=conversation_context)

        response = None
        for new_item in result.new_items:
            if isinstance(new_item, ToolCallOutputItem):
                response = new_item.output
                break
            elif isinstance(new_item, MessageOutputItem):
                response = ItemHelpers.text_message_output(new_item)

    return {
       "response": (
            response if isinstance(response, str)
            else str(response) if response is not None
            else "No response generated."
        )
    }


app.include_router(auth_routes.auth_router, prefix="/auth", tags=["auth"])
### Uvicorn entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
