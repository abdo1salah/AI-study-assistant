from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from pypdf import PdfReader
import os
import uuid # <--- 2. NEW IMPORT for unique IDs

embdedding_model = "mxbai-embed-large:335m"
embeddings = OllamaEmbeddings(model=embdedding_model)
db_location = "./vector_db"

def embedd_pdfs(file_paths, subject_name):
    # Initialize Vector Store
    vector_store = Chroma(
        collection_name="my_collection", 
        embedding_function=embeddings, 
        persist_directory=f'./subjects/{subject_name}/'+subject_name+'_chroma_db'
    )
    
    # Initialize Text Splitter
    # chunks of 1000 characters with 200 overlap is a standard starting point
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    raw_documents = []

    # 1. Load and create raw documents
    for file_path in file_paths:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Create a single document for the whole file first
        doc = Document(
            page_content=text,
            metadata={"source": os.path.basename(file_path)}
        )
        raw_documents.append(doc)

    # 2. Split the raw documents into smaller chunks
    chunked_documents = text_splitter.split_documents(raw_documents)

    # 3. Generate unique IDs for the new chunks
    # We cannot use the filename alone anymore because one file = many chunks
    ids = [str(uuid.uuid4()) for _ in chunked_documents]

    # 4. Add the CHUNKED documents to the store
    print(f"Adding {len(chunked_documents)} chunks to the vector store...")
    vector_store.add_documents(chunked_documents, ids=ids)
    
    # Note: In newer LangChain Chroma versions, persist() is often automatic, 
    # but we can keep it if your version requires it.
    # vector_store.persist()
 
def get_retriever(subject_name):
    vector_store = Chroma(
        collection_name="my_collection", 
        embedding_function=embeddings, 
        persist_directory=f'./subjects/{subject_name}/'+subject_name+'_chroma_db'
    )
    return vector_store.as_retriever(search_kwargs={"k": 3})