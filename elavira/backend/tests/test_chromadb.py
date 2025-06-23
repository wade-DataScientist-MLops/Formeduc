import chromadb
import pytest
from sentence_transformers import SentenceTransformer


@pytest.fixture(scope="module")
def client():
    # Client persistant avec stockage local
    return chromadb.PersistentClient(path="./chroma_data")


@pytest.fixture(scope="module")
def model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@pytest.fixture(scope="module")
def collection(client):
    collection_name = "formeduc_secourisme"
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
    return client.get_or_create_collection(name=collection_name)


def test_index_and_query_single_doc(collection, model):
    text = (
        "Formation de secourisme en ligne disponible pour tous. "
        "Certification reconnue conforme au règlement et à la loi."
    )
    embedding = model.encode([text]).tolist()
    collection.add(
        documents=[text],
        metadatas=[{"source": "test"}],
        ids=["doc1"],
        embeddings=embedding,
    )

    docs = collection.get()["documents"]
    print(f"Nombre de documents indexés : {len(docs)}")
    assert len(docs) > 0

    query = "Quelles formations de secourisme sont offertes en ligne ?"
    query_embedding = model.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=3)
    print("Résultats de la requête :", results)

    assert len(results["documents"][0]) > 0
    assert any(
        kw in results["documents"][0][0].lower()
        for kw in ["formation", "secourisme", "en ligne"]
    )


def test_index_multiple_documents(collection, model):
    texts = [
        "Formation de secourisme en ligne disponible pour tous.",
        "Certification reconnue conforme au règlement et à la loi.",
        "Cours de premiers soins adaptés à la petite enfance.",
        "Renouvellement de secourisme en milieu scolaire.",
        "Prévention de la maltraitance des enfants."
    ]
    embeddings = model.encode(texts).tolist()
    metadatas = [{"source": f"doc{i+1}"} for i in range(len(texts))]
    ids = [f"id{i+1}" for i in range(len(texts))]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

    docs = collection.get()["documents"]
    print(f"Nombre total de documents indexés : {len(docs)}")
    assert len(docs) >= len(texts)

    query = "Quelles formations de secourisme sont disponibles ?"
    query_embedding = model.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=3)
    print("Résultats de la requête :", results)

    assert len(results["documents"][0]) > 0
