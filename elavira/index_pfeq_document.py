# Fichier: index_pfeq_document.py
import os
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

# Pour éviter le warning parallelism Huggingface (optionnel)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Initialisation du client ChromaDB ---
# Le chemin d'accès est corrigé pour être relatif au répertoire du script.
# Ce script est à la racine du projet (elavira/), donc le chemin vers chroma_data est backend/chroma_data
script_dir = os.path.dirname(os.path.abspath(__file__))
chroma_db_path = os.path.join(script_dir, "backend", "chroma_data")
os.makedirs(chroma_db_path, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=chroma_db_path)
# Assurez-vous que le nom de la collection correspond à celui utilisé dans votre backend
collection = chroma_client.get_or_create_collection(name="elavira_collection")
print(f"✅ ChromaDB persistant à : {os.path.abspath(chroma_db_path)}")

# --- Initialisation du modèle d'embeddings SentenceTransformer ---
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedder (SentenceTransformer 'all-MiniLM-L6-v2') initialisé.")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de SentenceTransformer : {e}")
    raise RuntimeError(f"Échec de l'initialisation de l'embedder : {e}")

# --- Fonctions pour indexer les documents dans Chroma ---
def index_documents(texts: list[str], ids: list[str] = None):
    """
    Indexe une liste de textes dans la collection ChromaDB.
    """
    if not texts:
        print("Aucun texte à indexer.")
        return []
    
    # Générer les embeddings
    embeddings = embedder.encode(texts).tolist()
    
    # Générer les IDs si non fournis
    if ids is None:
        current_count = collection.count()
        ids = [f"doc_{current_count + i}" for i in range(len(texts))]
    
    # Ajouter les documents à la collection
    collection.add(documents=texts, embeddings=embeddings, ids=ids)
    print(f"✅ {len(texts)} documents indexés dans ChromaDB.")
    return ids

def load_pdf_and_index(pdf_file_path: str):
    """
    Charge un document PDF, extrait son texte, le découpe en morceaux
    et l'indexe dans la collection ChromaDB.
    """
    print(f"Chargement du document PDF : {pdf_file_path}")
    text_content = []
    try:
        reader = PdfReader(pdf_file_path)
        for page in reader.pages:
            text_content.append(page.extract_text())
        
        full_text = "\n".join(text_content)
        if not full_text.strip():
            print("Le PDF est vide ou n'a pas pu être extrait.")
            return

        # Découpage simple du texte en morceaux (chunks)
        # Ceci est un exemple basique. Pour de très grands documents,
        # vous pourriez vouloir une stratégie de découpage plus avancée.
        chunks = []
        current_chunk = ""
        # Découpe par paragraphes et limite la taille des morceaux
        for paragraph in full_text.split('\n'):
            # Évite d'ajouter des lignes vides ou des espaces blancs comme des morceaux
            if paragraph.strip(): 
                # Si le morceau actuel + le paragraphe dépasse la limite, ajoute le morceau actuel
                # et commence un nouveau morceau avec le paragraphe
                if len(current_chunk) + len(paragraph) + 1 > 1000: # +1 pour l'espace
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + " "
                else:
                    current_chunk += paragraph + " "
        # Ajoute le dernier morceau s'il n'est pas vide
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        print(f"Extrait {len(chunks)} morceaux de texte du PDF.")
        
        # Indexation des morceaux dans ChromaDB
        index_documents(chunks)
        print("Contenu du PDF indexé avec succès dans ChromaDB.")

    except Exception as e:
        print(f"❌ Erreur lors du chargement ou de l'indexation du PDF : {e}")

if __name__ == "__main__":
    # Chemin vers votre document PDF, relatif à la racine du projet 'elavira/'
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'PFEQ-secondaire-premier-cycle.pdf')
    
    if os.path.exists(pdf_path):
        load_pdf_and_index(pdf_path)
    else:
        print(f"❌ Erreur : Le fichier PDF n'a pas été trouvé à l'emplacement : {pdf_path}")
        print("Veuillez vérifier le chemin ou déplacer le fichier PDF.")

