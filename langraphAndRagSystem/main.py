from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
import shutil
import uvicorn  # ✅ import uvicorn to run the server

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Create FastAPI app
app = FastAPI()

# Allow CORS (so frontend can access it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint: PDF + Question → Answer
@app.post("/ask")
async def ask_question(file: UploadFile = File(...), question: str = Form(...)):
    # Save uploaded PDF
    pdf_path = f"temp_{file.filename}"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load PDF content
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # Chunk
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)

    # Vector DB from embeddings
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=GOOGLE_API_KEY
    )
    vectorstore = FAISS.from_documents(chunks, embedding)

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, streaming=False
    )

    # RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # Get answer
    result = qa_chain.invoke({"query": question})

    # Cleanup
    os.remove(pdf_path)

    return {
        "answer": result["result"],
        "sources": [doc.page_content[:300] for doc in result["source_documents"]]
    }

# ✅ Run with `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
