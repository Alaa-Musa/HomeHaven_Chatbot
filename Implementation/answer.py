from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
from langchain_community.callbacks import get_openai_callback
from datetime import datetime

from dotenv import load_dotenv


load_dotenv(override=True)

MODEL = "gpt-4.1-nano"
DB_NAME = str(Path(__file__).parent.parent / "vector_db")

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
RETRIEVAL_K = 5

SYSTEM_PROMPT = """
You are an expert question answerer for HomeHaven, a retailer of home goods.
You have access to a retriever that can retrieve relevant information about HomeHaven from a vector database.
Use the retriever to find relevant information and answer the user's question as accurately as possible.
If you don't know the answer, say you don't know. Do not make up an answer.
Context:
{context}
"""

vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        'k': RETRIEVAL_K,       # Number of documents to eventually return
    }    
)

llm = ChatOpenAI(temperature=0, model_name=MODEL)


def fetch_context(question: str) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    return retriever.invoke(question)


def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question




def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document], dict]:
    """
    Answer the given question with RAG; return answer, context, and usage stats.
    """
    # Wrap everything in the callback context manager
    with get_openai_callback() as cb:
        # Step 1: Query Refinement (This also uses tokens!)
        combined = combined_question(question, history)
        
        # Step 2: Context Retrieval
        docs = fetch_context(combined)
        context = "\n\n".join(doc.page_content for doc in docs)
        
        # Step 3: Final LLM Invocation
        system_prompt = SYSTEM_PROMPT.format(context=context)
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(convert_to_messages(history))
        messages.append(HumanMessage(content=question))
        
        response = llm.invoke(messages)
        
        # Gather stats into a dictionary
        usage_stats = {
            "total_tokens": cb.total_tokens,
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens,
            "total_cost_usd": cb.total_cost
        }
        
    return response.content, docs, usage_stats



def answer_question_pure_llm(question: str, full_knowledge_base: str, history: list = []) -> tuple[str, list, dict]:
    system_content = f"You are an expert assistant. Use the following knowledge base to answer:\n\n{full_knowledge_base}"
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] DEBUG: Knowledge Base Length: {len(full_knowledge_base)} characters")

    # Convert to LangChain objects
    messages = [SystemMessage(content=system_content)]
    messages.extend(convert_to_messages(history)) # Use your existing helper
    messages.append(HumanMessage(content=question))

    with get_openai_callback() as cb:
        response = llm.invoke(messages)
        usage_stats = {
            "total_tokens": cb.total_tokens,
            "prompt_tokens": cb.prompt_tokens,  # Add this to see the 50k
            "total_cost_usd": cb.total_cost
        }
    return response.content, [], usage_stats
