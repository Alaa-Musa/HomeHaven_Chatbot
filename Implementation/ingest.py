"""
RAG Knowledge Base Ingestion Module

This module handles the ingestion of markdown documents from the KnowledgeBase directory
into a Chroma vector database. It processes documents, chunks them, creates embeddings
using OpenAI's model, and stores them for retrieval-augmented generation (RAG) tasks.

The workflow:
1. Fetch all markdown files from organized knowledge base folders
2. Split documents into chunks for better embedding
3. Generate embeddings using OpenAI's text-embedding-3-large model
4. Store embeddings in a persistent Chroma vector database
"""

import os
import glob
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

# Model configuration for LLM responses
MODEL = "gpt-4.1-nano"

# Path to the persistent vector database directory
DB_NAME = str(Path(__file__).parent.parent / "vector_db")

# Path to the knowledge base directory containing all markdown files organized by category
KNOWLEDGE_BASE = str(Path(__file__).parent.parent / "KnowledgeBase")

# Load environment variables (API keys) from .env file
load_dotenv(override=True)

# Initialize embeddings using OpenAI's text-embedding-3-large model
# This model creates high-quality embeddings for semantic search
# Alternative: HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") for local embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def fetch_documents():
    """
    Load all markdown documents from the knowledge base directory.
    
    This function recursively scans each folder in the KNOWLEDGE_BASE directory
    and loads all .md files. Each document is tagged with its folder category
    as metadata for filtering/tracking during retrieval.
    
    Folder structure example:
    - KnowledgeBase/
        - Customer_Support/
        - Internal_Ops/
        - Policies_Legal/
        - product_catalog/
        - etc.
    
    Returns:
        list: A list of LangChain Document objects with 'doc_type' metadata
    """
    folders = glob.glob(str(Path(KNOWLEDGE_BASE) / "*"))
    documents = []
    for folder in folders:
        # Extract the folder name as document type (category)
        doc_type = os.path.basename(folder)
        
        # Create a loader for all markdown files in this folder and subfolders
        loader = DirectoryLoader(
            folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
        )
        folder_docs = loader.load()
        
        # Add metadata to track document source/category
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    
    return documents


def create_chunks(documents):
    """
    Split documents into smaller chunks for better embedding and retrieval.
    
    Large documents are split into overlapping chunks to:
    - Improve semantic relevance (each chunk has focused context)
    - Fit within embedding model token limits
    - Enable more precise retrieval (users find most relevant chunks)
    
    Parameters:
        chunk_size (int): 1500 characters per chunk (typical: 512-2000)
        chunk_overlap (int): 200 character overlap between chunks
                            Prevents losing context at chunk boundaries
    
    Args:
        documents (list): List of LangChain Document objects
    
    Returns:
        list: List of split Document chunks with metadata preserved
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_embeddings(chunks):
    """
    Convert chunks into embeddings and store in Chroma vector database.
    
    This function:
    1. Deletes any existing vector store to ensure fresh data
    2. Generates embeddings for each chunk using OpenAI's text-embedding-3-large
    3. Stores embeddings in a persistent Chroma database
    4. Verifies and displays database statistics
    
    The vector database enables fast semantic similarity search:
    - User queries are embedded using the same model
    - Database returns chunks with highest cosine similarity
    
    Args:
        chunks (list): List of Document chunks from create_chunks()
    
    Returns:
        Chroma: The vector store object for querying
    """
    # Delete existing database to ensure fresh ingestion
    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME, embedding_function=embeddings).delete_collection()

    # Create vector store by embedding all chunks and storing them
    # This may take time depending on chunk count and OpenAI API rate limits
    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=DB_NAME
    )

    # Verify database contents and display statistics
    collection = vectorstore._collection
    count = collection.count()

    # Get embedding dimensions to verify model is working correctly
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")
    
    return vectorstore


if __name__ == "__main__":
    # Execute the complete ingestion pipeline
    print("Starting knowledge base ingestion...")
    
    # Step 1: Load all markdown documents from knowledge base folders
    documents = fetch_documents()
    print(f"Loaded {len(documents)} documents")
    
    # Step 2: Split documents into smaller, overlapping chunks
    chunks = create_chunks(documents)
    print(f"Created {len(chunks)} chunks")
    
    # Step 3: Generate embeddings and store in vector database
    create_embeddings(chunks)
    
    print("Ingestion complete! Vector database is ready for querying.")
