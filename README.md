# RAG for Retailer - HomeHaven Chatbot

A Retrieval-Augmented Generation (RAG) system for an e-commerce retailer chatbot that answers customer support questions using an organized knowledge base.

## Project Overview

This project implements a smart customer support chatbot that:
- Retrieves relevant information from a structured knowledge base
- Augments queries with contextual information before generating responses
- Uses OpenAI embeddings for semantic search
- Provides a user-friendly Gradio interface for interaction and evaluation

## Project Structure

```
RAG_for_Retailer/
├── Implementation/
│   ├── ingest.py           # Ingestion pipeline (STEP 1)
│   ├── answer.py           # RAG query and response logic
│   └── __pycache__/
├── Evaluation/
│   ├── eval.py             # Evaluation metrics
│   ├── test.py             # Test utilities
│   └── tests.jsonl         # Test dataset
├── KnowledgeBase/          # Organized markdown documents
│   ├── Customer_Support/
│   ├── Internal_Ops/
│   ├── Policies_Legal/
│   ├── product_catalog/
│   ├── Programs_Services/
│   └── Reference_Tech/
├── KnowledgeBase_backup/   # Backup of original documents
├── vector_db/              # Chroma vector database (auto-generated)
├── notebooks/              # Analysis and experimentation notebooks
├── app.py                  # Alternative application interface
├── evaluator.py            # Gradio app for testing (STEP 2)
├── requirements.txt        # Python dependencies
├── environment.yml         # Conda environment file
├── pyproject.toml          # Project configuration
└── README.md              # This file
```

## Prerequisites

- Python 3.8+
- OpenAI API key
- Git (for version control)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Alaa-Musa/HomeHaven_Chatbot.git
cd RAG_for_Retailer
```

### 2. Create a Virtual Environment (Optional but Recommended)

Using `venv`:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

Or using `conda`:
```bash
conda env create -f environment.yml
conda activate rag-retailer
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

The `.env` file is ignored by git for security purposes.

## Quick Start

### Step 1: Ingest Knowledge Base

Run the ingestion pipeline to process documents and create embeddings:

```bash
python Implementation/ingest.py
```

**What this does:**
- Loads all markdown files from the `KnowledgeBase/` folder
- Splits documents into chunks (1500 characters with 200 character overlap)
- Generates embeddings using OpenAI's `text-embedding-3-large` model
- Stores embeddings in a persistent Chroma vector database (`vector_db/`)

**Output:** You'll see a message like:
```
There are X,XXX vectors with 3,072 dimensions in the vector store
Ingestion complete! Vector database is ready for querying.
```

### Step 2: Launch the Gradio Application

Once ingestion is complete, start the evaluator application:

```bash
python evaluator.py
```

**What this does:**
- Starts a Gradio web interface
- Allows you to input customer questions
- Retrieves relevant documents from the vector database
- Generates responses using the RAG system
- Displays retrieved sources and evaluation metrics

**Access the app:**
- Open your browser and navigate to the URL shown in the terminal (typically `http://localhost:7860`)
- Enter your questions and test the chatbot

## Usage Examples

### Running the Full Pipeline

```bash
# Terminal 1: Ingest knowledge base (run once)
cd c:\Users\mom_e\Projects\RAG_for_Retailer
python Implementation/ingest.py

# Terminal 2: Start the Gradio app
python evaluator.py
```

### Testing the System

The system includes evaluation tools in the `Evaluation/` folder:
```bash
python Evaluation/eval.py          # Run evaluation metrics
python Evaluation/test.py          # Run tests
```

## Configuration

### Embedding Model

The system uses OpenAI's `text-embedding-3-large` model. To change it, edit `Implementation/ingest.py`:

```python
# For smaller embeddings (faster, uses less memory):
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# For local embeddings (free, no API key needed):
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

### Chunk Size

Adjust chunk size and overlap in `Implementation/ingest.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,      # Change to 1000-2000 characters
    chunk_overlap=200     # Change to 0-500 characters
)
```

### LLM Model

Change the LLM model in `Implementation/ingest.py`:

```python
MODEL = "gpt-4.1-nano"  # Change to "gpt-4", "gpt-3.5-turbo", etc.
```

## Key Components

### `Implementation/ingest.py`
Handles knowledge base ingestion, document loading, chunking, and embedding storage.

**Functions:**
- `fetch_documents()` - Load markdown files from knowledge base folders
- `create_chunks()` - Split documents into overlapping chunks
- `create_embeddings()` - Generate embeddings and store in vector database

### `Implementation/answer.py`
Implements the RAG query logic and response generation.

### `evaluator.py`
Gradio-based web interface for testing and evaluating the system.

### `Evaluation/eval.py`
Evaluation metrics and performance analysis.

## Troubleshooting

### "OpenAI API key not found"
- Ensure your `.env` file exists in the root directory
- Check that `OPENAI_API_KEY` is set correctly
- Verify the API key is valid on the OpenAI dashboard

### "Vector database not found"
- Run `python Implementation/ingest.py` first to create the database
- Ensure the `vector_db/` folder is created in the root directory

### Out of memory during ingestion
- Reduce `chunk_size` in `ingest.py` (e.g., from 1500 to 1000)
- Use a smaller embedding model like `text-embedding-3-small`

### Slow API responses
- The first ingestion takes longer due to OpenAI API rate limits
- Subsequent queries use local vector search and are much faster

## Contributing

To contribute improvements:

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -am 'Add new feature'`
3. Push to the branch: `git push origin feature/your-feature`
4. Submit a pull request

## Performance Notes

- **Ingestion:** Depends on knowledge base size and OpenAI API limits (typically minutes)
- **Query Response:** Local vector search is fast (<1 second), LLM generation takes 2-5 seconds
- **Vector DB Size:** Approximately 100-500 MB depending on knowledge base size

## License

This project is part of the HomeHaven customer support system.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Last Updated:** March 9, 2026
