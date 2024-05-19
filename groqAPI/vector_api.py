import chromadb
import json

import time
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
ef = SentenceTransformerEmbeddingFunction(model_name="thenlper/gte-small", device="cuda")


# query_text = "kartik from the congress"
# query_embeddings = [query_text]

collection_name = "unique_values"
collection = chromadb.PersistentClient("./ChromaStuff/dataStore/").get_collection(collection_name)


def get_closest_docs_to_summary(summary):
    query_embeddings = [summary]
    results = collection.query(
        query_embeddings=ef(query_embeddings),
        n_results = 10
    )
    # print(results["documents"][0])
    return results["documents"][0]
    
