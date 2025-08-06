# core/vector_store_solenys.py
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

def index_solenys_pdf():
    loader = PyPDFLoader("PFEQ-secondaire-premier-cycle.pdf")
    documents = loader.load_and_split()
    
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(
        documents,
        embedding,
        persist_directory="chroma_data/solenys"
    )
    vectordb.persist()
    print("✅ Base vectorielle Solenys indexée.")
