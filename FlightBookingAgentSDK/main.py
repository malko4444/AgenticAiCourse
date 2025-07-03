import os
import uuid
from dataclasses import dataclass
from dotenv import load_dotenv
from fastapi import FastAPI, Request,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from config.dataBase import db
from tools.flight_agent_tool import simple_flight_booking, user_all_flights,faq_lookup_tool,cancel_booking
from fastapi.responses import JSONResponse
from routes import auth_routes
from utils.utils import verify_token
from validation.validation import AirlineAgentContext

from agents import (
    Agent,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    ToolCallOutputItem,
    TResponseInputItem,
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
- location (departure and destination)
- Date of Flight
status (default is "booked") 
- Passport Number
- Login User ID 

You will use the `simple_flight_booking` tool to confirm the booking.

When the user provides their full name,passport number, and other booking details, you must extract the following information:
1. Full Name: The complete name of the passenger.
2. Passport Number: The passport number of the passenger.
3. Location: The departure and destination locations for the flight.
4. Date: The date of the flight.



Always try to extract this information from the user’s input, even if it's in natural or unstructured language.

Once you have all four required pieces of information, call the `simple_flight_booking` tool immediately to confirm the booking.

If any information is missing, ask *only* for the missing details — do not repeat or ask again for already known values.
and when you call the tool in the user input it also have login user id and the email so we can store the booking against a specific user and send the otp code to the user email
and if user demand to see all the flights that are booked by him then use the `user_all_flights` tool to get all the flights that are booked by him and return it to the user.
if user want to cancel the flight booking then use the `cancel_booking` tool to cancel the flight booking and return the message to the user.
user input have _id , login_user_id and login_user_email so we can use it to cancel the booking and send the otp code to the user email.
"""
,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[simple_flight_booking,user_all_flights, cancel_booking],
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
async def chat_with_agent(request: Request,user_from_token=Depends(verify_token)):
    global input_items, current_agent
    print(f"User ID: that are stored in the db {user_from_token.get('user_id')}")



    user_input = await request.body()
    # embed user_from_token with the user input so the llm provide it to the agent
    user_input = user_input + f"\nlogin_User_iD: {user_from_token.get('user_id')}".encode("utf-8")
    user_input = user_input + f"\nuser_email: {user_from_token.get('user_email')}".encode("utf-8")
    print(f"User input received after decode the token : {user_from_token.get('user_id')}")
    conversation_context.login_user_id = user_from_token.get('user_id')
    print(f"Conversation context updated with user ID: {conversation_context}")
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


@app.get("/user_flights")
async def get_user_flights(user_from_token=Depends(verify_token)):
    """
    Get all flights booked by the user.
    """
    login_user_id = user_from_token.get('user_id')
    if not login_user_id:
        return JSONResponse(status_code=400, content={
            "message": "User ID is required.",
            "status": "error",
            "data": None
        })

    # Find all bookings for the given user ID
    bookings = db.bookings.find({"login_user_id": login_user_id})

    user_flights = []
    for booking in bookings:
        booking["_id"] = str(booking["_id"])  # Convert ObjectId to string
        user_flights.append(booking)

    return {
        "data": {
            "user_flights": user_flights
        },
        "message": "User flights retrieved successfully",
        "status": "success"
    }
app.include_router(auth_routes.auth_router, prefix="/auth", tags=["auth"])
### Uvicorn entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
