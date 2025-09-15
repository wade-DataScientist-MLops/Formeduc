#!/usr/bin/env python3
"""
Script pour indexer les documents PFEQ dans ChromaDB
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from chroma_client import collection, embedder, index_documents

def index_pfeq_documents():
    """
    Indexe les documents PFEQ dans ChromaDB
    """
    print("📚 Indexation des documents PFEQ...")
    
    # Documents PFEQ de base
    pfeq_documents = [
        {
            "content": """
            PROGRAMME DE FORMATION DE L'ÉCOLE QUÉBÉCOISE (PFEQ)
            
            MATHEMATIQUES - SECONDAIRE 1
            
            Compétences disciplinaires:
            1. Résoudre une situation-problème mathématique
            2. Déployer un raisonnement mathématique
            3. Communiquer à l'aide du langage mathématique
            
            Contenu de formation:
            - Nombres naturels et décimaux
            - Opérations arithmétiques de base
            - Géométrie plane et solide
            - Mesures et unités
            - Probabilités et statistiques
            - Algèbre élémentaire
            """,
            "metadata": {"subject": "mathématiques", "level": "secondaire 1", "source": "pfeq"}
        },
        {
            "content": """
            PROGRAMME DE FORMATION DE L'ÉCOLE QUÉBÉCOISE (PFEQ)
            
            FRANÇAIS - SECONDAIRE 1-2
            
            Compétences disciplinaires:
            1. Lire et apprécier des textes variés
            2. Écrire des textes variés
            3. Communiquer oralement selon des modalités variées
            
            Contenu de formation:
            - Grammaire et syntaxe
            - Littérature québécoise et francophone
            - Analyse de textes
            - Rédaction et composition
            - Communication orale
            - Stratégies de lecture et d'écriture
            """,
            "metadata": {"subject": "français", "level": "secondaire 1-2", "source": "pfeq"}
        },
        {
            "content": """
            PROGRAMME DE FORMATION DE L'ÉCOLE QUÉBÉCOISE (PFEQ)
            
            SCIENCES ET TECHNOLOGIE - SECONDAIRE 1-2
            
            Compétences disciplinaires:
            1. Chercher des réponses ou des solutions à des problèmes d'ordre scientifique ou technologique
            2. Mettre à profit ses connaissances scientifiques et technologiques
            3. Communiquer à l'aide des langages utilisés en science et technologie
            
            Contenu de formation:
            - Univers matériel (physique, chimie)
            - Terre et espace (géologie, astronomie)
            - Univers vivant (biologie, écologie)
            - Techniques et instrumentation
            - Applications technologiques
            
            CHIMIE - COMPOSITION DE L'EAU:
            L'eau (H2O) est composée de:
            - 2 atomes d'hydrogène (H)
            - 1 atome d'oxygène (O)
            - Liaison covalente polaire
            - Masse molaire: 18 g/mol
            - Point d'ébullition: 100°C
            - Point de fusion: 0°C
            - Solvant universel
            """,
            "metadata": {"subject": "sciences", "level": "secondaire 1-2", "source": "pfeq"}
        },
        {
            "content": """
            PROGRAMME DE FORMATION DE L'ÉCOLE QUÉBÉCOISE (PFEQ)
            
            HISTOIRE ET ÉDUCATION À LA CITOYENNETÉ - SECONDAIRE 1-2
            
            Compétences disciplinaires:
            1. Interroger les réalités sociales dans une perspective historique
            2. Interpréter les réalités sociales à l'aide de la méthode historique
            3. Construire sa conscience citoyenne à l'aide de l'histoire
            
            Contenu de formation:
            - Histoire du Québec (Nouvelle-France à aujourd'hui)
            - Histoire mondiale (civilisations, événements marquants)
            - Géographie du Québec et du monde
            - Éducation à la citoyenneté
            - Méthodes de recherche historique
            """,
            "metadata": {"subject": "histoire", "level": "secondaire 1-2", "source": "pfeq"}
        },
        {
            "content": """
            PROGRAMME DE FORMATION DE L'ÉCOLE QUÉBÉCOISE (PFEQ)
            
            GÉOGRAPHIE - SECONDAIRE 1-2
            
            Compétences disciplinaires:
            1. Construire sa conscience du territoire
            2. Interpréter un enjeu territorial
            3. Construire sa conscience citoyenne à l'aide de la géographie
            
            Contenu de formation:
            - Géographie physique du Québec
            - Géographie humaine du Québec
            - Géographie mondiale
            - Enjeux territoriaux contemporains
            - Cartographie et outils géographiques
            - Développement durable
            """,
            "metadata": {"subject": "géographie", "level": "secondaire 1-2", "source": "pfeq"}
        }
    ]
    
    # Extraire les contenus et métadonnées
    texts = [doc["content"] for doc in pfeq_documents]
    metadatas = [doc["metadata"] for doc in pfeq_documents]
    ids = [f"pfeq_{i+1}" for i in range(len(pfeq_documents))]
    
    # Indexer dans ChromaDB
    try:
        index_documents(texts, ids)
        print(f"✅ {len(pfeq_documents)} documents PFEQ indexés avec succès!")
        
        # Ajouter les métadonnées
        for i, metadata in enumerate(metadatas):
            collection.update(
                ids=[ids[i]],
                metadatas=[metadata]
            )
        
        print("✅ Métadonnées ajoutées aux documents PFEQ!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation: {e}")

if __name__ == "__main__":
    index_pfeq_documents()
