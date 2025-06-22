
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

import os
load_dotenv()

llm = GoogleGenerativeAI(
     model="gemini-1.5-flash",
     google_api_key=os.getenv("GOOGLE_API_KEY")
)
# from one time result
# result = llm.invoke("what is promp engineering in easy english ")

# print(result)
# streaming result
question= input("Enter your question: ")
for chunk in llm.stream(question):
    print(chunk, end="", flush=True)
