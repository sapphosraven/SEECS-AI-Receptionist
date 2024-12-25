#!/usr/bin/env python
# coding: utf-8

# In[1]:



# # Local RAG agent with LLaMA3
# 
# We'll combine ideas from paper RAG papers into a RAG agent:
# 
# - **Routing:**  Adaptive RAG ([paper](https://arxiv.org/abs/2403.14403)). Route questions to different retrieval approaches
# - **Fallback:** Corrective RAG ([paper](https://arxiv.org/pdf/2401.15884.pdf)). Fallback to web search if docs are not relevant to query
# - **Self-correction:** Self-RAG ([paper](https://arxiv.org/abs/2310.11511)). Fix answers w/ hallucinations or don’t address question
# 
# ![langgraph_adaptive_rag.png](attachment:6cd777a6-a0b3-4feb-bd07-8e9e8a4b32a0.png)
# 
# ## Local models
# 
# ### Embedding
#  
# [GPT4All Embeddings](https://blog.nomic.ai/posts/nomic-embed-text-v1):
# 
# ```
# pip install langchain-nomic
# ```
# 
# ### LLM
# 
# Use [Ollama](https://x.com/ollama/status/1839007158865899651) and [llama3.2](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/):
# 
# ```
# ollama pull llama3.2:3b-instruct-fp16 
# ```

# In[1]:


from langchain.schema import HumanMessage
from langchain_ollama import ChatOllama
import torch 

# Initialize the Llama model
#local_llm = "llama3.1:8b"
#llm = ChatOllama(model=local_llm, temperature=0, device="cuda")
#llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json", device="cuda")

# Test the LLM with a properly formatted message
#message = [HumanMessage(content="What is the significance of AI in modern technology?")]

# Generate a response
#response = llm(message)
#print(response.content)


# ### Search
# 
# For search, we use [Tavily](https://tavily.com/), which is a search engine optimized for LLMs and RAG.

# In[2]:


import os

def _set_env(var: str, value: str):
    if not os.environ.get(var):
        os.environ[var] = value

_set_env("TAVILY_API_KEY", "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")
_set_env("LANGSMITH_API_KEY", "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")
os.environ["TOKENIZERS_PARALLELISM"] = "true"


# ### Tracing 
# 
# Optionally, use [LangSmith](https://www.langchain.com/langsmith) for tracing. 

# In[4]:


#_set_env("LANGSMITH_API_KEY", "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")
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_PROJECT"] = "local-llama32-rag"


# ### Vectorstore 

# In[3]:

import os
import pickle
import fitz  # PyMuPDF
import torch
import faiss
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS

# Paths for storing embeddings and metadata
VECTOR_STORE_INDEX_PATH = r"F:\Uni Stuff\5th Sem\AI\Project\SEECS-AI-Receptionist\LLM\RAG-DATA\faiss_index"
VECTOR_STORE_METADATA_PATH = r"F:\Uni Stuff\5th Sem\AI\Project\SEECS-AI-Receptionist\LLM\RAG-DATA\faiss_metadata.pkl"
EMBEDDINGS_CACHE_PATH = r"F:\Uni Stuff\5th Sem\AI\Project\SEECS-AI-Receptionist\LLM\RAG-DATA\embeddings.pkl"

# Set GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
torch.backends.cudnn.benchmark = True  # Optimize GPU performance for repetitive tasks

# Initialize the LLM on GPU
# Global instances for persistent usage
local_llm = "llama3.1:8b"
global_llm = ChatOllama(model=local_llm, temperature=0, device="cuda" if torch.cuda.is_available() else "cpu")
global_llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json", device="cuda" if torch.cuda.is_available() else "cpu")


# Function to load PDFs from a folder
def load_pdfs_from_folder(folder_path):
    pdf_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                pdf_texts.append(text)
    return pdf_texts

# Function to save embeddings to a cache
def save_embeddings(embeddings, texts, path=EMBEDDINGS_CACHE_PATH):
    with open(path, "wb") as f:
        pickle.dump({"embeddings": embeddings, "texts": texts}, f)
#    print("Embeddings saved to disk.")

# Function to load cached embeddings
def load_embeddings(path=EMBEDDINGS_CACHE_PATH):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = pickle.load(f)
#        print("Embeddings loaded from disk.")
        return data["embeddings"], data["texts"]
    else:
#        print("No cached embeddings found.")
        return None, None

# Function to initialize or reinitialize the vectorstore
def initialize_vectorstore():
    """Initialize the FAISS vectorstore and save it to disk."""
    if os.path.exists(VECTOR_STORE_INDEX_PATH):
#        print("Vectorstore already exists. Delete the files if you want to reinitialize.")
        return load_vectorstore()

#    print("Initializing vectorstore...")
    # Load and process PDF documents
    rag_data_folder = r"F:\Uni Stuff\5th Sem\AI\Project\SEECS-AI-Receptionist\LLM\RAG-DATA\RAG-DATA"
    pdf_docs = load_pdfs_from_folder(rag_data_folder)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    doc_splits = text_splitter.split_documents([Document(page_content=doc) for doc in pdf_docs])
    texts = [doc.page_content for doc in doc_splits]

    # Load cached embeddings or create new ones
    embeddings, cached_texts = load_embeddings()
    if embeddings is None or cached_texts != texts:
#        print("No cached embeddings found or texts have changed. Generating embeddings...")
        embedding_model = OllamaEmbeddings(model="llama3.1:8b")
        embeddings = embedding_model.embed_documents(texts)
        save_embeddings(embeddings, texts)  # Save the new embeddings

    # Create FAISS vectorstore
    embedding_model = OllamaEmbeddings(model="llama3.1:8b")
    vectorstore = FAISS.from_texts(texts=texts, embedding=embedding_model)

    # Move FAISS index to GPU for faster retrieval
    res = faiss.StandardGpuResources()
    gpu_index = faiss.index_cpu_to_gpu(res, 0, vectorstore.index)
    vectorstore.index = gpu_index

    # Move index back to CPU before saving
    cpu_index = faiss.index_gpu_to_cpu(vectorstore.index)
    vectorstore.index = cpu_index

    # Save FAISS index
    vectorstore.save_local(VECTOR_STORE_INDEX_PATH)

    # Save metadata (e.g., document texts)
    with open(VECTOR_STORE_METADATA_PATH, "wb") as f:
        pickle.dump({"document_texts": texts}, f)

#    print("Vectorstore initialized and saved to disk.")
    return vectorstore

# Function to load an existing vectorstore
def load_vectorstore():
    """Load the FAISS vectorstore from disk."""
#    print("Loading vectorstore from disk...")

    # Initialize the embedding model
    embedding_model = OllamaEmbeddings(model="llama3.1:8b")

    # Load FAISS vectorstore
    vectorstore = FAISS.load_local(
        VECTOR_STORE_INDEX_PATH,
        embedding_model,
        allow_dangerous_deserialization=True  # Enable pickle deserialization
    )

    # Move FAISS index to GPU
    res = faiss.StandardGpuResources()
    gpu_index = faiss.index_cpu_to_gpu(res, 0, vectorstore.index)
    vectorstore.index = gpu_index

    # Load metadata
    with open(VECTOR_STORE_METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
        vectorstore.document_texts = metadata["document_texts"]

    print("Vectorstore loaded successfully.")
    return vectorstore

# Initialize or load the vectorstore
# Retriever can also be made global to avoid repeated initialization
if os.path.exists(VECTOR_STORE_INDEX_PATH) and os.path.exists(VECTOR_STORE_METADATA_PATH):
    global_vectorstore = load_vectorstore()
else:
    global_vectorstore = initialize_vectorstore()

global_retriever = global_vectorstore.as_retriever(k=3)

'''
# Initialize or load the FAISS vectorstore
def initialize_vectorstore():
    """Initialize the FAISS vectorstore and save it to disk."""
    if os.path.exists(VECTOR_STORE_INDEX_PATH):
        print("Vectorstore already exists. Delete the files if you want to reinitialize.")
        return load_vectorstore()

    print("Initializing vectorstore...")
    # Load and process PDF documents
    rag_data_folder = "RAG-DATA"
    pdf_docs = load_pdfs_from_folder(rag_data_folder)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    doc_splits = text_splitter.split_documents([Document(page_content=doc) for doc in pdf_docs])

    # Generate embeddings using the embedding model
    embedding_model = OllamaEmbeddings(model="llama3.1:8b")
    texts = [doc.page_content for doc in doc_splits]

    # Generate embeddings
    if not os.path.exists(EMBEDDINGS_CACHE_PATH):
        print("No cached embeddings found.")
        embeddings = embedding_model.embed_documents(texts)
        with open(EMBEDDINGS_CACHE_PATH, "wb") as f:
            pickle.dump(embeddings, f)
        print("Embeddings saved to disk.")
    else:
        print("Loading cached embeddings.")
        with open(EMBEDDINGS_CACHE_PATH, "rb") as f:
            embeddings = pickle.load(f)

    # Create FAISS vectorstore
    vectorstore = FAISS.from_texts(texts=texts, embedding=embedding_model)

    # Save FAISS index
    vectorstore.save_local(VECTOR_STORE_INDEX_PATH)

    # Save metadata (e.g., document texts)
    with open(VECTOR_STORE_METADATA_PATH, "wb") as f:
        pickle.dump({"document_texts": texts}, f)

    print("Vectorstore initialized and saved to disk.")
    return vectorstore




# Load the FAISS vectorstore from disk

def load_vectorstore():
    """Load the FAISS vectorstore from disk."""
    print("Loading vectorstore from disk...")

    # Initialize the embedding model
    embedding_model = OllamaEmbeddings(model="llama3.1:8b")

    # Load FAISS vectorstore with deserialization enabled
    vectorstore = FAISS.load_local(
        VECTOR_STORE_INDEX_PATH,
        embedding_model,
        allow_dangerous_deserialization=True  # Enable pickle deserialization
    )

    # Load metadata
    with open(VECTOR_STORE_METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
        vectorstore.document_texts = metadata["document_texts"]

    print("Vectorstore loaded successfully.")
    return vectorstore


# Initialize or load the vectorstore
if os.path.exists(VECTOR_STORE_INDEX_PATH) and os.path.exists(VECTOR_STORE_METADATA_PATH):
    vectorstore = load_vectorstore()
else:
    vectorstore = initialize_vectorstore()

# Set up the retriever
retriever = vectorstore.as_retriever(k=3)

'''


'''
import os
import fitz  # PyMuPDF
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_ollama import OllamaEmbeddings  # Updated import for OllamaEmbeddings
import pickle

def load_pdfs_from_folder(folder_path):
    pdf_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                pdf_texts.append(text)
    return pdf_texts

VECTOR_STORE_PATH = "vectorstore.pkl"

def initialize_vectorstore():
    """Initialize the vectorstore and save it to disk."""
    if os.path.exists(VECTOR_STORE_PATH):
        print("Vectorstore already exists. Delete the file if you want to reinitialize.")
        return load_vectorstore()  # Return the loaded vectorstore instead of None

    print("Initializing vectorstore...")
    # Load and process PDF documents
    rag_data_folder = "RAG-DATA"
    pdf_docs = load_pdfs_from_folder(rag_data_folder)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    doc_splits = text_splitter.split_documents([Document(page_content=doc) for doc in pdf_docs])

    # Generate embeddings using the embedding model
    embedding_model = OllamaEmbeddings(model="llama3.1:8b")
    embeddings = embedding_model.embed_documents([doc.page_content for doc in doc_splits])

    # Create the vectorstore
    vectorstore = SKLearnVectorStore(embedding=embedding_model)
    vectorstore.add_texts(
        texts=[doc.page_content for doc in doc_splits],
        embeddings=embeddings,
    )

    # Save only the document texts and embeddings (serializable data)
    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump({
            "embeddings": embeddings,
            "document_texts": [doc.page_content for doc in doc_splits],
        }, f)

    print("Vectorstore initialized and saved to disk.")
    return vectorstore

def load_vectorstore():
    """Load the vectorstore from disk."""
    print("Loading vectorstore from disk...")
    with open(VECTOR_STORE_PATH, "rb") as f:
        data = pickle.load(f)

    # Reconstruct the vectorstore from saved data
    embedding_model = OllamaEmbeddings(model="llama3.1:8b")  # Re-initialize embedding model
    vectorstore = SKLearnVectorStore(embedding=embedding_model)
    vectorstore.add_texts(
        texts=data["document_texts"],
        embeddings=data["embeddings"],
    )
    return vectorstore

# Initialize or load vectorstore
if os.path.exists(VECTOR_STORE_PATH):
    vectorstore = load_vectorstore()  # Load from disk if it exists
else:
    vectorstore = initialize_vectorstore()  # Initialize and save if not

# Set up the retriever
retriever = vectorstore.as_retriever(k=3)
'''


# In[4]:


# Test retriever
#query = "Tell me about SEECS."
#retrieved_docs = retriever.get_relevant_documents(query)
#for i, doc in enumerate(retrieved_docs, 1):
    #print(f"Document {i}:\n{'-'*50}\n{doc.page_content.strip()}\n")


# In[ ]:





# In[ ]:





# In[ ]:





# ### Components

# In[5]:


### Router
import json
from langchain_core.messages import HumanMessage, SystemMessage

# Prompt
router_instructions = """You are an expert AI receptionist at SEECS, NUST (Islamabad, Pakistan).

Your goal is to guide users and answer all their questions related to SEECS and NUST only.

This includes information about programmes being offered, the professors, the facilities, the timetables etc.

You also are able to route a user question to a vectorstore or websearch.

The vectorstore contains documents related to SEECS and NUST in general.

Use the vectorstore for questions on topics related to SEECS. For all else:
- If the question is about you (e.g., "Who are you?"), respond with: "I am an AI receptionist at SEECS, NUST, here to assist you with any questions related to SEECS or NUST."
- If you do not have a concise and accurate answer about SEECS or NUST, answer that you do not know. Do not come up with something on your own.

You may do a websearch for things ONLY related to SEECS and NUST.

If a personal question is asked, tell that you are a helpful AI receptionist for SEECS and nothing else.

Return JSON with a single key, datasource, that is 'websearch' or 'vectorstore' depending on the question.
"""

# Test router
test_web_search = global_llm_json_mode.invoke(
    [SystemMessage(content=router_instructions)]
    + [
        HumanMessage(
            content="When do admissions open for the undergraduate programs at SEECS?"
        )
    ]
)
test_web_search_2 = global_llm_json_mode.invoke(
    [SystemMessage(content=router_instructions)]
    + [HumanMessage(content="What courses are offered at SEECS?")]
)
test_vector_store = global_llm_json_mode.invoke(
    [SystemMessage(content=router_instructions)]
    + [HumanMessage(content="What are the rules a student must follow?")]
)
#print(
 #   json.loads(test_web_search.content),
  #  json.loads(test_web_search_2.content),
   # json.loads(test_vector_store.content),
#)


# In[6]:


### Retrieval Grader

# Doc grader instructions
doc_grader_instructions = """You are a grader assessing relevance of a retrieved document to a user question.

If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant."""

# Grader prompt
doc_grader_prompt = """Here is the retrieved document: \n\n {document} \n\n Here is the user question: \n\n {question}. 

This carefully and objectively assess whether the document contains at least some information that is relevant to the question.

Return JSON with single key, binary_score, that is 'yes' or 'no' score to indicate whether the document contains at least some information that is relevant to the question."""

# Test
question = "Tell me about the Computer Science department at SEECS."
docs = global_retriever.invoke(question)
doc_txt = docs[1].page_content
doc_grader_prompt_formatted = doc_grader_prompt.format(
    document=doc_txt, question=question
)
result = global_llm_json_mode.invoke(
    [SystemMessage(content=doc_grader_instructions)]
    + [HumanMessage(content=doc_grader_prompt_formatted)]
)
json.loads(result.content)


# In[8]:


### Generate

# Prompt
rag_prompt = """You are an AI receptionist responsible for question-answering tasks. 

Here is the context to use to answer the question:

{context} 

Think carefully about the above context. 

Now, review the user question:

{question}

Provide an answer to this questions using only the above context. 

Use three sentences maximum and keep the answer concise. Do not talk about which file you got answer from.

Answer:"""


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Test
docs = global_retriever.invoke(question)
docs_txt = format_docs(docs)
rag_prompt_formatted = rag_prompt.format(context=docs_txt, question=question)
generation = global_llm.invoke([HumanMessage(content=rag_prompt_formatted)])
#print(generation.content)


# In[9]:


# Hallucination grader instructions
hallucination_grader_instructions = """
You are an evaluator for an AI receptionist system.

You will be given CONTEXT (facts or retrieved documents) and an AI RESPONSE.

Here is the grade criteria to follow:

(1) Ensure the AI RESPONSE is grounded in the CONTEXT provided. 

(2) Ensure the AI RESPONSE does not contain "hallucinated" information outside the scope of the CONTEXT.

Score:

A score of yes means that the AI RESPONSE meets all of the criteria. This is the highest (best) score.

A score of no means that the AI RESPONSE does not meet all of the criteria. This is the lowest possible score.

Explain your reasoning step-by-step to ensure your reasoning and conclusion are correct.

Avoid simply stating the correct answer at the outset. Provide reasoning to justify the score.
"""

# Grader prompt
hallucination_grader_prompt = """
CONTEXT: \n\n {documents} \n\n AI RESPONSE: {generation}. 

Return JSON with two keys: binary_score ('yes' or 'no') to indicate whether the AI RESPONSE is grounded in the CONTEXT, and explanation, which contains an explanation of the score.
"""

# Test using documents and generation from above
hallucination_grader_prompt_formatted = hallucination_grader_prompt.format(
    documents=docs_txt, generation=generation.content
)

# Invoke the LLM
result = global_llm_json_mode.invoke(
    [SystemMessage(content=hallucination_grader_instructions)]
    + [HumanMessage(content=hallucination_grader_prompt_formatted)]
)

# Parse the result
#print(json.loads(result.content))


# In[10]:


# Answer grader instructions
answer_grader_instructions = """
You are an evaluator for an AI receptionist system.

You will be given a USER QUESTION and an AI RESPONSE.

Here is the grade criteria to follow:

(1) The AI RESPONSE must effectively and accurately answer the USER QUESTION.

(2) The AI RESPONSE can include extra relevant information, as long as it does not deviate from the scope of the USER QUESTION.

Score:

A score of yes means that the AI RESPONSE meets all of the criteria. This is the highest (best) score.

A score of no means that the AI RESPONSE does not meet all of the criteria. This is the lowest possible score.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct.

Avoid simply stating the correct answer at the outset. Provide reasoning to justify the score.
"""

# Grader prompt
answer_grader_prompt = """
USER QUESTION: \n\n {question} \n\n AI RESPONSE: {generation}. 

Return JSON with two keys: binary_score ('yes' or 'no') to indicate whether the AI RESPONSE meets the criteria, and explanation, which contains an explanation of the score.
"""

# Test
question = "What courses are offered at SEECS?"
answer = "SEECS offers a variety of courses, including Computer Science, Software Engineering, Electrical Engineering, and Information Technology. It also provides specialized programs in AI and Data Science."

# Format the prompt using the question and answer
answer_grader_prompt_formatted = answer_grader_prompt.format(
    question=question, generation=answer
)

# Invoke the LLM
result = global_llm_json_mode.invoke(
    [SystemMessage(content=answer_grader_instructions)]
    + [HumanMessage(content=answer_grader_prompt_formatted)]
)

# Parse the result
#print(json.loads(result.content))


# ## Web Search Tool

# In[11]:


### Search
from langchain_community.tools.tavily_search import TavilySearchResults

web_search_tool = TavilySearchResults(k=3)


# # Graph 
# 
# We build the above workflow as a graph using [LangGraph](https://langchain-ai.github.io/langgraph/).
# 
# ### Graph state
# 
# The graph `state` schema contains keys that we want to:
# 
# * Pass to each node in our graph
# * Optionally, modify in each node of our graph 
# 
# See conceptual docs [here](https://langchain-ai.github.io/langgraph/concepts/low_level/#state).

# In[27]:


import operator
from typing_extensions import TypedDict
from typing import List, Annotated


class GraphState(TypedDict):
    """
    Graph state is a dictionary that contains information we want to propagate to, and modify in, each graph node.
    """

    question: str  # User question
    generation: str  # LLM generation
    web_search: str  # Binary decision to run web search
    max_retries: int  # Max number of retries for answer generation
    answers: int  # Number of answers generated
    loop_step: Annotated[int, operator.add]
    documents: List[str]  # List of retrieved documents


# In[64]:


from langchain.schema import Document
from langgraph.graph import END


### Nodes
def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    #print("---RETRIEVE---")
    try:
        question = state["question"]
        documents = global_retriever.invoke(question)
        return {"documents": documents}
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return {"documents": []}


def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    #print("---GENERATE---")
    question = state["question"]
    documents = state.get("documents", [])
    loop_step = state.get("loop_step", 0)

    if not documents:
        print("No relevant documents available for generation.")
        return {"generation": "I'm sorry, I couldn't find relevant information.", "loop_step": loop_step + 1}

    responses = []
    try:
        for doc_chunk in documents:
            docs_txt = format_docs([doc_chunk])
            rag_prompt_formatted = rag_prompt.format(context=docs_txt, question=question)
            response = global_llm.invoke([HumanMessage(content=rag_prompt_formatted)])
            responses.append(response.content.strip())
        combined_response = "\n".join(responses)
        return {"generation": combined_response, "loop_step": loop_step + 1}
    except Exception as e:
        print(f"Error during generation: {e}")
        return {"generation": "Error generating response.", "loop_step": loop_step + 1}


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    #print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state.get("documents", [])

    if not documents:
        print("No documents retrieved for grading.")
        return {"documents": [], "web_search": "Yes"}

    # Score each doc
    filtered_docs = []
    web_search = "No"
    for d in documents:
        doc_grader_prompt_formatted = doc_grader_prompt.format(
            document=d.page_content, question=question
        )
        result = global_llm_json_mode.invoke(
            [SystemMessage(content=doc_grader_instructions)]
            + [HumanMessage(content=doc_grader_prompt_formatted)]
        )
        grade = json.loads(result.content)["binary_score"]
        # Document relevant
        if grade.lower() == "yes":
            #print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        # Document not relevant
        else:
            #print("---GRADE: DOCUMENT NOT RELEVANT---")
            # We do not include the document in filtered_docs
            # We set a flag to indicate that we want to run web search
            web_search = "Yes"
            continue
    return {"documents": filtered_docs, "web_search": web_search}


def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    #print("---WEB SEARCH---")
    question = state["question"]
    documents = state.get("documents", [])

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    documents.append(web_results)
    return {"documents": documents}


### Edges

def route_question(state):
    """
    Route question to web search or RAG

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    #print("---ROUTE QUESTION---")
    route_question = global_llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content=state["question"])]
    )
    source = json.loads(route_question.content)["datasource"]
    if source == "websearch":
        #print("---ROUTE QUESTION TO WEB SEARCH---")
        return "websearch"
    elif source == "vectorstore":
        #print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or add web search

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    #print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    web_search = state["web_search"]
    filtered_documents = state["documents"]

    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        #print(
            #"---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        #)
        return "websearch"
    else:
        # We have relevant documents, so generate answer
        #print("---DECISION: GENERATE---")
        return "generate"


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    #print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    max_retries = state.get("max_retries", 3)  # Default to 3 if not provided

    hallucination_grader_prompt_formatted = hallucination_grader_prompt.format(
        documents=format_docs(documents), generation=generation.content
    )
    result = global_llm_json_mode.invoke(
        [SystemMessage(content=hallucination_grader_instructions)]
        + [HumanMessage(content=hallucination_grader_prompt_formatted)]
    )
    grade = json.loads(result.content)["binary_score"]

    # Check hallucination
    if grade == "yes":
        #print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        #print("---GRADE GENERATION vs QUESTION---")
        # Test using question and generation from above
        answer_grader_prompt_formatted = answer_grader_prompt.format(
            question=question, generation=generation.content
        )
        result = global_llm_json_mode.invoke(
            [SystemMessage(content=answer_grader_instructions)]
            + [HumanMessage(content=answer_grader_prompt_formatted)]
        )
        grade = json.loads(result.content)["binary_score"]
        if grade == "yes":
            #print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        elif state["loop_step"] <= max_retries:
            #print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
        else:
            #print("---DECISION: MAX RETRIES REACHED---")
            return "max retries"
    elif state["loop_step"] <= max_retries:
        #print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
    else:
        #print("---DECISION: MAX RETRIES REACHED---")
        return "max retries"
    



# Each node in our graph is simply a function that:
# 
# (1) Take `state` as an input
# 
# (2) Modifies `state` 
# 
# (3) Write the modified `state` to the state schema (dict)
# 
# See conceptual docs [here](https://langchain-ai.github.io/langgraph/concepts/low_level/#nodes).
# 
# Each edge routes between nodes in the graph.
# 
# See conceptual docs [here](https://langchain-ai.github.io/langgraph/concepts/low_level/#edges).

# ## Control Flow

# In[48]:


from langgraph.graph import StateGraph
from IPython.display import Image, display

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search)  # web search
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generate

# Build graph
workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "websearch",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_edge("retrieve", "grade_documents")

workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
        "max retries": END,
    },
)


# Compile
graph = workflow.compile()
#display(Image(graph.get_graph().draw_mermaid_png()))


# In[63]:


# Inputs specific to SEECS AI Receptionist
#inputs = {
 #   "question": "What programs are offered at SEECS?",  # Example user question
  #  "max_retries": 3,  # Maximum retries allowed for generating a relevant response
#}

# Stream the workflow execution and display the events
#for event in graph.stream(inputs, stream_mode="values"):
    #print(event)


# Trace:
# 
# https://smith.langchain.com/public/1e01baea-53e9-4341-a6d1-b1614a800a97/r

# In[31]:


# Test on current events
#inputs = {
 #   "question": "Who is the head of the Computer Science department at SEECS?",
  #  "max_retries": 3,
#}
#for event in graph.stream(inputs, stream_mode="values"):
    #print(event)


# In[51]:


personal_question_prompt = """
You are an AI model helping an AI receptionist at SEECS, NUST. 

Classify whether the following question is personal or related to SEECS:

Question: {question}

Return JSON with a single key "is_personal" and value "yes" or "no".
"""


# In[66]:


import json
def run_ai_receptionist(question: str, debug=False) -> str:
    """
    Executes the SEECS AI Receptionist workflow and returns a final response.

    Args:
        question (str): The user's question to the AI receptionist.
        debug (bool): If True, enables debug messages for troubleshooting.

    Returns:
        str: The final response generated by the AI receptionist.
    """
    global global_llm, global_llm_json_mode, global_retriever

    # Detect if the question is personal
    detect_personal_prompt = personal_question_prompt.format(question=question)
    try:
        detection_response = global_llm_json_mode.invoke(
            [HumanMessage(content=detect_personal_prompt)]
        )
        is_personal = json.loads(detection_response.content).get("is_personal", "no")
    except Exception as e:
        if debug:
            print(f"Error detecting personal question: {e}")
        is_personal = "no"

    # Handle personal questions
    if is_personal == "yes":
        try:
            personal_response_prompt = f"""
            You are an AI receptionist at SEECS, NUST. Answer the following personal question appropriately:

            Question: {question}

            Answer in one or two sentences.
            """
            personal_response = global_llm.invoke(
                [HumanMessage(content=personal_response_prompt)]
            )
            return personal_response.content.strip()
        except Exception as e:
            if debug:
                print(f"Error generating personal response: {e}")
            return "I'm sorry, I couldn't process your personal question."

    # Define inputs for workflow
    inputs = {
        "question": question,
        "max_retries": 3,
    }
    
    # Initialize variable for final output
    final_output = None

    # Stream the workflow execution
    try:
        for event in graph.stream(inputs, stream_mode="values"):
            if debug:
                print("---WORKFLOW EVENT---", event)
            if "generation" in event:
                final_output = event["generation"].content.strip()

        # Resetting state to avoid cross-query conflicts
        graph.reset_state()
        return final_output or "No response generated."
    except Exception as e:
        if debug:
            print(f"Unexpected error during workflow: {e}")
        graph.reset_state()
        return "I'm sorry, there was an error processing your request."

    if debug:
        print(f"Initial state: {inputs}")

    try:
        for event in graph.stream(inputs, stream_mode="values"):
            if debug:
                print("---WORKFLOW EVENT---", event)
            if "generation" in event:
                final_output = event["generation"].content.strip()

        if debug and not final_output:
            print("No valid output generated by the workflow.")

    except Exception as e:
        if debug:
            print(f"Unexpected error during workflow: {e}")
        return "I'm sorry, there was an error processing your request."

    return final_output or "No response generated."




# In[69]:


def model_inference(question: str) -> str:
    """
    Wrapper for the run_ai_receptionist function to extract the clean output.

    Args:
        question (str): The user's question to the AI receptionist.

    Returns:
        str: The processed response output.
    """
    try:
        # Call the AI receptionist function
        response = run_ai_receptionist(question)
        
        # Clean and return the response
        return response.strip() if response else "No response generated."
    except Exception as e:
        return f"Error during inference: {e}"


# In[67]:


# Example question
question = "Who are you?"

# Run the AI receptionist and get the final output
#response = run_ai_receptionist(question)

# Print the response
#print(response)


# In[72]:


# Example question
#question = "Tell me all about SEECS?"

# Run the AI receptionist and get the final output
#response = run_ai_receptionist(question)

# Print the response
#print(f"Output: {response}")


# In[74]:


# Example question
#question = "Name a few societies in NUST"

# Run the AI receptionist and get the final output
#response = run_ai_receptionist(question)

# Print the response
#print(f"Output: {response}")


# Trace:
# 
# https://smith.langchain.com/public/acdfa49d-aa11-48fb-9d9c-13a687ff311f/r

# 
