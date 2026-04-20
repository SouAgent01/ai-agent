# rag_test.py
# Phase 5 - First RAG pipeline

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
print("All imports successful!")

# Section 2 - Create a sample document and split into chunks
document = """
CICS (Customer Information Control System) is a transaction server that runs 
on IBM mainframes. It manages online transactions for thousands of users 
simultaneously. CICS handles task management, storage management, and 
communication between programs.

JCL (Job Control Language) is used to define batch jobs on the mainframe.
It tells the operating system what programs to run, what data to use, and
what to do with the output. Every mainframe batch job starts with JCL.

VSAM (Virtual Storage Access Method) is a file access method used on IBM
mainframes. It supports three types of datasets: KSDS (key-sequenced),
ESDS (entry-sequenced), and RRDS (relative record). VSAM is the primary
way to store and retrieve structured data on z/OS.

Ollama is a local LLM server for macOS and Linux. It downloads and serves
AI models locally on your hardware. No cloud, no API keys, no cost per query.
It exposes a REST API on port 11434 that any program can call.

ChromaDB is a vector database designed for AI applications. It stores text
alongside its embedding vectors and enables semantic search. Instead of
finding exact keyword matches, ChromaDB finds documents with similar meaning.
"""

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

chunks = splitter.split_text(document)

print(f"Document split into {len(chunks)} chunks")
for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i}:")
    print(chunk)

# Section 3 - Store chunks in ChromaDB with embeddings
import os

print("\nCreating embeddings and storing in ChromaDB...")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Only create if database doesn't exist yet
if os.path.exists("./chroma_db"):
    print("ChromaDB already exists - loading existing database")
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
else:
    print("Creating new ChromaDB database...")
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB!")

print("Database ready!")

# Section 4 - Search by meaning (semantic search)
print("\n--- Semantic Search Test ---")

questions = [
    "What handles online transactions on the mainframe?",
    "How do I run batch jobs?",
    "What stores data locally without internet?",
]

for question in questions:
    print(f"\nQuestion: {question}")
    results = vectorstore.similarity_search(question, k=2)
    for i, doc in enumerate(results, 1):
        print(f"Result {i}: {doc.page_content[:100]}...")

# Section 5 - Full RAG Pipeline
print("\n--- Full RAG Pipeline ---")

import ollama as ollama_client

question = "What is CICS transaction server and what does it manage?"

# Step 1: retrieve and SHOW what chunks were found
docs = vectorstore.similarity_search(question, k=3)
print("Chunks retrieved for this question:")
for i, doc in enumerate(docs, 1):
    print(f"  Chunk {i}: {doc.page_content[:80]}...")

context = "\n".join([doc.page_content for doc in docs])

# Step 2: send to LLM with context
prompt = f"""Use the following context to answer the question.
Only use information from the context provided.

Context:
{context}

Question: {question}

Answer:"""

response = ollama_client.chat(
    model='llama3.2:3b',
    messages=[{'role': 'user', 'content': prompt}]
)

print(f"\nQuestion: {question}")
print(f"\nAnswer: {response['message']['content']}")