"""
Module for managing note documents and FAISS vector indexing using LangChain.

Functions:
    - load_documents(): Load text documents from the specified directory.
    - create_faiss_index(): Create and save a FAISS vector index for document embeddings.
    - search_notes(): Search the vector index for relevant text chunks.
    - read_file(): Read the student's progress report from a text file.
    - write_file(): Overwrite the progress report with new content.
"""

import glob
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import INDEX_PATH, NOTES_DIR, TOPICS_DIR, PROGRESS_DIR


# Document loading
def load_documents(notes_dir: str):
    """
    Load all text documents from the specified directory.

    Args:
        notes_dir (str): The path pattern to the directory containing text files.

    Returns:
        list: A list of loaded langchain document objects.
    """
    docs = []
    for file_path in glob.glob(notes_dir):
        loader = TextLoader(file_path)
        docs.extend(loader.load())
    return docs


# FAISS index creation
def create_faiss_index(docs: list, index_path: str, embeddings_model=None) -> None:
    """
    Create and save a FAISS index from the given documents.

    Args:
        docs (list): List of LangChain Document objects.
        index_path (str): Directory path to save the FAISS index.
        embeddings_model: Optional; a pre-initialised embeddings model.

    Returns:
        None
    """
    # Use the OpenAI embeddings model
    if embeddings_model is None:
        embeddings_model = OpenAIEmbeddings()  # ensure OPENAI_API_KEY is in .env

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=200, 
        is_separator_regex=False,
        )
    
    chunks = text_splitter.split_documents(docs)

    # Create and save the FAISS index
    vectorstore = FAISS.from_documents(chunks, embeddings_model)
    vectorstore.save_local(index_path)
    print(f"Saved FAISS index to {index_path}")
    return

# Function to return a string containing the formatted search results.
def search_notes(query: str) -> str:  
    '''
    This tool let's you search through the set of notes to find information relevant to the topic the student is studying.
    Use this when creating questions, answering question, or marking questions for the student. The query should be very specific 
    keywords or phrases only, e.g. if the topic being studied was mutable data types then the query would be: list, dictionary, set, adding elements etc...

    Args:
        query: Specific keywords, or phrases to search for.
        
    Returns: 
        str: Relevant text chunks from the notes that match the query.
    '''
    # Load the FAISS index and embeddings model 
    embeddings_model = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        INDEX_PATH, 
        embeddings_model, 
        allow_dangerous_deserialization=True,
    )
    
    # Retrieve the 4 most relevant chunks
    docs = vectorstore.similarity_search(query, k=4)  
    
    # Format the results
    if not docs:
        return "No relevant information found in the notes."
    
    results = []
    for i, doc in enumerate(docs):
        content = doc.page_content
        source = doc.metadata.get('source', 'Unknown source')
        results.append(f"--- Result {i+1} from {source} ---\n{content}\n")
    
    return "\n".join(results)


# Function to read the contents of a .txt file
def read_file():
    """
    Reads the entire content of the progress report which is a text file containing the details of what topics the 
    student is struggling with, and the date when that information was added to the text file.
    Returns:
        str: The content in the text file
    """
    try:
        with open(PROGRESS_DIR, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error reading file: {e}"

# Function to overwrire the contents of a .txt file
def write_file(content: str) -> str:
    """
    Overwrites the content of the progress report with new content.

    Args: 
        content (str): The string of content that you want to be put into the .txt file.
    Return:
        str: A message to say whether or not the file was successfully updated.
    """
    try:
        with open(PROGRESS_DIR, "w", encoding="utf-8") as f:
            f.write(content)
        return "File successfully updated."
    except Exception as e:
        return f"Error writing to file: {e}"
    