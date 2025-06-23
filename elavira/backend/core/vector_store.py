from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

def index_secourisme_file():
    file_path = "backend/data/secourisme.txt"

    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    # Couper le texte en morceaux
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Générer les embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Charger la base Chroma
    db = Chroma(persist_directory="backend/chroma_data", embedding_function=embeddings)

    # Ajouter les documents
    db.add_documents(docs)
    db.persist()

    print("✅ Texte indexé dans ChromaDB.")
 
 