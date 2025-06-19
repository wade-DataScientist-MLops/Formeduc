import chromadb
import os

def get_chroma_client(persistent: bool = False, path: str = "./chroma_db"):
    """
    Retourne un client ChromaDB.

    Args:
        persistent (bool): Si True, retourne un client persistant qui stocke les données sur le disque.
                           Si False, retourne un client en mémoire (les données sont perdues à la fermeture).
        path (str): Le chemin du répertoire pour stocker les données ChromaDB si 'persistent' est True.
                    Par défaut à "./chroma_db" dans le répertoire de travail actuel.

    Returns:
        chromadb.Client: Un client ChromaDB en mémoire.
        chromadb.PersistentClient: Un client ChromaDB persistant.
    """
    if persistent:
        # S'assurer que le répertoire existe
        os.makedirs(path, exist_ok=True)
        print(f"Client ChromaDB persistant initialisé, les données seront stockées à : {os.path.abspath(path)}")
        return chromadb.PersistentClient(path=path)
    else:
        print("Client ChromaDB en mémoire initialisé (les données ne seront pas persistantes).")
        return chromadb.Client()

def get_collection(client, name="elavira_collection"):
    """
    Récupère ou crée une collection dans le client ChromaDB donné.

    Args:
        client (chromadb.Client ou chromadb.PersistentClient): L'instance du client ChromaDB.
        name (str): Le nom de la collection.

    Returns:
        chromadb.api.models.Collection: La collection ChromaDB.
    """
    return client.get_or_create_collection(name)

# Exemple d'utilisation :

if __name__ == "__main__":
    # --- Utilisation d'un client en mémoire ---
    print("\n--- Utilisation du client ChromaDB en mémoire ---")
    in_memory_client = get_chroma_client(persistent=False)
    in_memory_collection = get_collection(in_memory_client, "ma_collection_en_memoire")

    in_memory_collection.add(
        documents=["Ceci est un document sur les données en mémoire.", "Un autre document temporaire."],
        metadatas=[{"source": "test"}, {"source": "temp"}],
        ids=["doc1", "doc2"]
    )
    print(f"Documents dans la collection en mémoire : {in_memory_collection.count()}")

    # --- Utilisation d'un client persistant ---
    print("\n--- Utilisation du client ChromaDB persistant ---")
    # Vous voudrez peut-être définir un chemin spécifique pour vos données persistantes
    # Par exemple, relatif à l'emplacement de votre script
    script_dir = os.path.dirname(__file__)
    persistent_db_path = os.path.join(script_dir, "elavira_chroma_data")

    persistent_client = get_chroma_client(persistent=True, path=persistent_db_path)
    persistent_collection = get_collection(persistent_client, "elavira_collection")

    # Ajouter des données à la collection persistante
    if persistent_collection.count() == 0: # Éviter d'ajouter des doublons lors des réexécutions
        persistent_collection.add(
            documents=["Ceci est un document persistant.", "Des données qui restent sur le disque."],
            metadatas=[{"auteur": "moi"}, {"statut": "enregistré"}],
            ids=["doc_pers_1", "doc_pers_2"]
        )
        print("Documents ajoutés à la collection persistante.")
    else:
        print("La collection persistante contient déjà des données. Ignorer l'ajout.")

    print(f"Documents dans la collection persistante : {persistent_collection.count()}")

    # Vous pouvez interroger la collection
    results = persistent_collection.query(
        query_texts=["données persistantes"],
        n_results=1
    )
    print("\nRésultats de la requête de la collection persistante :")
    print(results)

    # Pour nettoyer les données persistantes pour les tests, vous pouvez supprimer le répertoire :
    # import shutil
    # if os.path.exists(persistent_db_path):
    #     print(f"\nNettoyage des données persistantes à : {persistent_db_path}")
    #     shutil.rmtree(persistent_db_path)