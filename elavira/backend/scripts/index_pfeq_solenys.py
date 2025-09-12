#!/usr/bin/env python3
"""
Script pour indexer le document PFEQ dans ChromaDB pour Solenys
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from core.solenys_logic import get_solenys_chroma_client, get_solenys_embedder

def index_pfeq_document():
    """Indexe le document PFEQ dans ChromaDB pour Solenys"""
    
    # Chemin vers le document PFEQ
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pfeq_path = os.path.join(script_dir, "..", "PFEQ-secondaire-premier-cycle.pdf")
    
    if not os.path.exists(pfeq_path):
        print(f"❌ Document PFEQ non trouvé : {pfeq_path}")
        print("Veuillez placer le fichier PFEQ-secondaire-premier-cycle.pdf dans le dossier backend/")
        return False
    
    try:
        # Importer PyPDF2 pour lire le PDF
        from PyPDF2 import PdfReader
        
        print(f"📖 Lecture du document PFEQ : {pfeq_path}")
        
        # Lire le PDF
        reader = PdfReader(pfeq_path)
        text_content = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                text_content.append(f"Page {page_num + 1}: {text}")
        
        full_text = "\n\n".join(text_content)
        
        if not full_text.strip():
            print("❌ Le PDF est vide ou n'a pas pu être extrait")
            return False
        
        print(f"✅ Texte extrait : {len(full_text)} caractères")
        
        # Découper en chunks
        chunks = []
        current_chunk = ""
        chunk_size = 1000
        
        for paragraph in full_text.split('\n'):
            if paragraph.strip():
                if len(current_chunk) + len(paragraph) + 1 > chunk_size:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + " "
                else:
                    current_chunk += paragraph + " "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        print(f"📝 Chunks créés : {len(chunks)}")
        
        # Générer les embeddings
        embedder = get_solenys_embedder()
        if not embedder:
            print("❌ Erreur initialisation embedder")
            return False
        
        embeddings = embedder.encode(chunks).tolist()
        
        # Indexer dans ChromaDB
        collection = get_solenys_chroma_client()
        
        # Générer des IDs uniques
        ids = [f"solenys_pfeq_{i}" for i in range(len(chunks))]
        
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )
        
        print(f"✅ {len(chunks)} documents PFEQ indexés pour Solenys")
        return True
        
    except ImportError:
        print("❌ PyPDF2 non installé. Installez avec : pip install PyPDF2")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation : {e}")
        return False

if __name__ == "__main__":
    print("🚀 Indexation du document PFEQ pour Solenys...")
    success = index_pfeq_document()
    
    if success:
        print("🎉 Indexation terminée avec succès !")
        print("Solenys peut maintenant répondre selon le programme PFEQ du Québec.")
    else:
        print("💥 Échec de l'indexation.")
