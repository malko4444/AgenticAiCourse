
from config.dataBase import db
from agents import     function_tool

from utils.utils import verify_token, send_otp_email

    


@function_tool
async def user_all_flights(
    login_user_id: str | None = None,
) -> list[dict]:
    """ A tool to get all flights booked by a user.
    :param login_user_id: user ID for tracking and store a specific record against a particular user so we can get it when need 
    :return: A list of all flights booked by the user
    """
    if not login_user_id:
        return {"error": "User ID is required."}

    # Find all bookings for the given user ID
    bookings = db.bookings.find({"login_user_id": login_user_id})
    
    # Convert ObjectId to string for JSON serialization
    return [{"_id": str(booking["_id"]), **booking} for booking in bookings]

@function_tool
async def simple_flight_booking(
    passenger_name: str,
    passport_number: int,
    login_user_id: str | None = None,
    status: str = "booked",
    location: str | None = None,
    date: str | None = None,
   login_user_email: str | None = None,
    
):
    # await simple_flight_booking(..., user_id=conversation_context.user_id)
    """ A simple flight booking tool that checks if a seat is available and books it.
    :param passenger_name: Full name of the passenger
    :param passport_number: Passport number of the passenger
    :param login_user_id: user ID for tracking and store a specific record against a particular user so we can get it when need
    :param status: Status of the booking (default is "booked")
    :param location: location for the flight like Pakistan to canada
    :param date: date for the flight 
    :param login_user_email: user email for sending the otp code and it get from the user input 
    :return: A message indicating success or failure of the booking

    """
    # fetch record using login user id from the db to match after add the new booking
    existing_booking = db.bookings.find_one({"login_user_id": login_user_id,"location": location, "date": date})
    if existing_booking:
        return {
            "message": f"Flight already booked for {passenger_name} on {date} from {location}.",
            "booking_info": existing_booking
        }
    

    
    booking_info = {
        "passenger_name": passenger_name,
        "login_user_id": login_user_id,
        "passport_number": passport_number,
        "status": status,
        "location": location ,
        "date": date,

    }

    result =db.bookings.insert_one(booking_info)
    
    # result.inserted_id is the ObjectId of the inserted document
    print(f"Booking result: {result.inserted_id}")

    # Add the ObjectId as a string to the response
    booking_info["_id"] = str(result.inserted_id)
    receiver_message = f"Your flight has been booked successfully for {passenger_name} on {date} from {location}. Booking ID: {booking_info['_id']}."
    await send_otp_email(login_user_email,receiver_message)
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
# cancel booking just mark the status as cancelled and send the email to the user
@function_tool
async def cancel_booking(
    booking_id: str,
    login_user_id: str | None = None,
    login_user_email: str | None = None,
) -> dict:
    """ A tool to cancel a flight booking.
    :param booking_id: ID of the booking to cancel
    :param login_user_id: user ID for tracking and store a specific record against a particular user so we can get it when need
    :param login_user_email: user email for sending the otp code and it get from the user input 
    :return: A message indicating success or failure of the cancellation
    """
    print(f"Cancel booking called with booking_id: {booking_id}, login_user_id: {login_user_id}, login_user_email: {login_user_email}")
    # convert booking id into object to campare with the db record
    from bson import ObjectId
    try:
        booking_id = ObjectId(booking_id)
    except Exception as e:
        return {"error": "Invalid booking ID format."}
    # Find the booking by ID
    booking = db.bookings.find_one({"_id": booking_id, "login_user_id": login_user_id})
    
    if not booking:
        return {"error": "Booking not found."}
    
    # Update the status to "cancelled"
    db.bookings.update_one({"_id": booking["_id"]}, {"$set": {"status": "cancelled"}})
    
    # Send cancellation email
    cancellation_message = f"Your flight booking with ID {booking_id} has been cancelled."
    await send_otp_email(login_user_email, cancellation_message)
    
    return {"message": "Booking cancelled successfully."}
