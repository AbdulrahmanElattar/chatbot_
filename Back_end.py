import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from together import Together
from pydantic import BaseModel
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
import re
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


load_dotenv()

vectorstore = None
embeddings = None
PDF_FILE_NAME = "/media/elbooody/New_Volume/Chat_bot/Hands-On_Large_Language_Models-1.pdf"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorstore, embeddings
    
    if not os.path.exists(PDF_FILE_NAME):
        yield 
        return
    else:
        loader = PyPDFLoader(PDF_FILE_NAME)
        documents = loader.load()

        if not documents:
            vectorstore = None
            yield 
            return

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        separators=[". ", "? ", "! ", "\n\n", "\n", " ", ""]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=separators
        )

        splitted_documents = text_splitter.split_documents(documents)

        if not splitted_documents:
            vectorstore = None
            yield
            return

        
        list_of_sentences=[]
        for document in splitted_documents:
            tokenized_sent=nltk.sent_tokenize(document.page_content)
            for sent in tokenized_sent:
                sent=re.sub(r"\n",'',sent).strip()
                if not sent.strip() or  sent in separators:
                    continue
                list_of_sentences.append(sent)

        if list_of_sentences:
            vectorstore = FAISS.from_texts(list_of_sentences, embeddings)

        else:
            vectorstore = None

    yield
client = Together()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    user_id: str

class ChatResponse(BaseModel):
    answer: str
    usage: Dict[str, int]

app = FastAPI(lifespan=lifespan)



@app.post("/api/chat")
async def chat_with_llm(request: ChatRequest)->ChatResponse:
    if vectorstore is None:
        return ChatResponse(
            answer=f"Error: RAG system not initialized. Please ensure the PDF file exists at: {PDF_FILE_NAME}",
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )

    user_question = request.messages[-1].content if request.messages else ""

    if not user_question.strip():
        return ChatResponse(
            answer="Please provide a message to chat with the LLM.",
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )

    retrieved_docs = vectorstore.similarity_search(user_question, k=5)

    context_parts = [doc.page_content for doc in retrieved_docs]
    context = "\n\n".join(context_parts)

    augmented_messages = []

    system_message_content = (
        "You are a helpful and knowledgeable assistant. "
        "Answer the user's question based *only* on the following provided context. "
        "If the answer is not explicitly available in the context, state that you don't have enough information from the provided context.\n\n"
        "Here is the relevant context:\n"
        f"<context>\n{context}\n</context>"
    )
    augmented_messages.append({"role": "system", "content": system_message_content})

    for msg in request.messages[:-1]:
        augmented_messages.append({"role": msg.role, "content": msg.content})

    augmented_messages.append({"role": "user", "content": user_question})
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=augmented_messages,
        temperature=0.7,
        max_tokens=512
    )

    model_response = response.choices[0].message.content

    return ChatResponse(
        answer=model_response,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    )