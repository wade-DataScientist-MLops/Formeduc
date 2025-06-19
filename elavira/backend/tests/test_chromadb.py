import chromadb
from sentence_transformers import SentenceTransformer
import pytest

@pytest.fixture(scope="module")
def client():
    return chromadb.Client()

@pytest.fixture(scope="module")
def collection(client):
    return client.get_or_create_collection("elavira_collection")

@pytest.fixture(scope="module")
def model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def test_add_documents(collection, model):
    texts = ["Le chien aboie fort.", "Le chat dort paisiblement."]
    embeddings = model.encode(texts).tolist()
    metadatas = [{"source": "doc1"}, {"source": "doc2"}]
    ids = ["id1", "id2"]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

    assert len(collection.get()["documents"]) == 2

def test_query_documents(collection, model):
    query = "Quel animal aboie fort ?"
    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    assert len(results["documents"][0]) > 0
    assert "Le chien aboie fort." in results["documents"][0]
