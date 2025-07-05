from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Step 1: Load PDF
loader = PyPDFLoader("book.pdf")  # Replace with your actual PDF path
pages = loader.load()

# Step 2: Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(pages)

# Step 3: Create vector store
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY  # ✅ Pass the key here
)
vectorstore = FAISS.from_documents(chunks, embedding)

# Step 4: Setup LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,  # ✅ Pass the key here
    temperature=0,
    streaming=False

)

# Step 5: Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Step 6: Ask questions
while True:
    query = input("Ask a question about the PDF: ")
    if query.lower() in ["exit", "quit"]:
        break
    result = qa_chain.invoke({"query": query})
    print("\nAnswer:", result["result"])
    print("\n--- Source(s) ---")
    for doc in result["source_documents"]:
        print(doc.page_content[:300], "...\n")
