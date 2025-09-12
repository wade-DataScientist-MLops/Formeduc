#!/usr/bin/env python3
"""
Script simplifié pour indexer des données PFEQ de base pour Solenys
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

import chromadb
from sentence_transformers import SentenceTransformer

def index_pfeq_basic_data():
    """Indexe des données PFEQ de base pour Solenys"""
    
    try:
        # Initialiser ChromaDB
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chroma_db_path = os.path.join(script_dir, "..", "chroma_data")
        os.makedirs(chroma_db_path, exist_ok=True)
        
        client = chromadb.PersistentClient(path=chroma_db_path)
        collection = client.get_or_create_collection(name="elavira_collection")
        
        # Initialiser l'embedder
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Données PFEQ de base pour le secondaire
        pfeq_data = [
            "Le Programme de formation de l'école québécoise (PFEQ) définit les compétences à développer au secondaire.",
            "En mathématiques secondaire 1-2, les élèves apprennent les opérations de base, les fractions, les pourcentages et la géométrie.",
            "En mathématiques secondaire 3-4, les élèves étudient l'algèbre, les fonctions, la trigonométrie et les statistiques.",
            "En sciences secondaire 1-2, les élèves explorent la matière, l'énergie, les systèmes vivants et la Terre.",
            "En sciences secondaire 3-4, les élèves approfondissent la chimie, la physique, la biologie et l'environnement.",
            "En français secondaire, les élèves développent la lecture, l'écriture, la communication orale et la littérature.",
            "Le PFEQ privilégie l'approche par compétences plutôt que la mémorisation pure.",
            "Les évaluations au secondaire portent sur les compétences transversales et disciplinaires.",
            "Les compétences transversales incluent la communication, la coopération et la résolution de problèmes.",
            "Le curriculum québécois vise à préparer les élèves à la vie citoyenne et professionnelle."
        ]
        
        print(f"📚 Indexation de {len(pfeq_data)} éléments PFEQ de base...")
        
        # Générer les embeddings
        embeddings = embedder.encode(pfeq_data).tolist()
        
        # Générer des IDs uniques
        ids = [f"solenys_pfeq_basic_{i}" for i in range(len(pfeq_data))]
        
        # Indexer dans ChromaDB
        collection.add(
            documents=pfeq_data,
            embeddings=embeddings,
            ids=ids
        )
        
        print(f"✅ {len(pfeq_data)} éléments PFEQ indexés pour Solenys")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation : {e}")
        return False

if __name__ == "__main__":
    print("🚀 Indexation des données PFEQ de base pour Solenys...")
    success = index_pfeq_basic_data()
    
    if success:
        print("🎉 Indexation terminée avec succès !")
        print("Solenys peut maintenant répondre selon le programme PFEQ de base.")
    else:
        print("💥 Échec de l'indexation.")
