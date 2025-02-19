# Env variables loader
import os
import dotenv
dotenv.load_dotenv(dotenv_path="../../.env.shopping")

# Data handlers
import pandas as pd
from sqlalchemy.orm import Session

# Utils
try:
    from data_utils import get_db, get_restaurants, get_foods
    from data_models import Restaurant, Foods
    from database import SessionLocal
except:
    from .data_utils import get_db, get_restaurants, get_foods
    from .data_models import Restaurant, Foods
    from .database import SessionLocal

# LlamaIndex
from llama_index.core import (
    VectorStoreIndex,
    Document,
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.retrievers.bm25 import BM25Retriever

from llama_index.core.vector_stores import MetadataFilter, ExactMatchFilter
from llama_index.core.retrievers import BaseRetriever

# VDBs
import pinecone

# Local Pinecone settings
LOCAL_HOST = "http://localhost:5081"
LOCAL_API_KEY = "pclocal"
INDEX_NAME = "auto-food-order"

# Initialize Pinecone
pinecone_client = pinecone.Pinecone(api_key=LOCAL_API_KEY, environment="local")

# Create index with spec
index_spec = {
    "dimension": 1536,
    "metric": "cosine"
}
pinecone_client.create_index(
    name=INDEX_NAME,
    dimension=1536,
    metric="cosine"
)
def process_restaurants():
    # Reading SQLite db
    db = SessionLocal()
    restaurants = get_restaurants(db)
    foods = get_foods(db)

    # Convert the data to a pandas DataFrame
    restaurant_data = [{"id": r.id, "name": r.name, "description": r.description,} for r in restaurants]
    restaurant_df = pd.DataFrame(restaurant_data)

    food_data = [{"id": f.id, "restaurant_id": f.restaurant_id, "name": f.name, "description": f.description, "price": f.price} for f in foods]
    food_df = pd.DataFrame(food_data)

    # Processing for merge: renaming columns
    food_df = food_df.rename(
        columns={
            "id": "food_id",
            "restaurant_id": "id",
            "name": "food_name",
            "description": "food_description",
        }
    )

    # Merging
    df = pd.merge(restaurant_df, food_df, on="id")

    # Groupby restaurant and creating text for embedding
    df["food_text"] = "\n-"+df["food_name"] + "\n" + df["food_description"]

    df = df.groupby("id").agg({"name": "first", "description": "first", "food_text": "sum"}).reset_index()

    # Creating text for embedding
    df["text"] = "``````"

    # LlamaIndex
    documents = [
        Document(
            text=df_row[1]["text"],
            metadata={
                "search_type": "restaurant",
                "restaurant_id": df_row[1]["id"],
                "restaurant_name": df_row[1]["name"],
                "restaurant_description": df_row[1]["description"],
                "restaurant_menu": df_row[1]["food_text"],
            }
        )
        for df_row in df.iterrows()
    ]

    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        host=LOCAL_HOST,
        api_key=LOCAL_API_KEY,
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
    )

    llm = OpenAI(model="gpt-4")

    service_context = ServiceContext.from_defaults(chunk_size=512, llm=llm)

    node_parser = SimpleNodeParser.from_defaults()
    nodes = node_parser.get_nodes_from_documents(documents)

    storage_context.docstore.add_documents(nodes)

    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        service_context=service_context,
    )

    return index, nodes

def load_index():
    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        host=LOCAL_HOST,
        api_key=LOCAL_API_KEY,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex([], storage_context=storage_context)

    return index

def main():
    # Testing it
    index, nodes = process_restaurants()
    idx = load_index()

    ret = idx.as_retriever(similarity_top_k=5)
    ret2 = idx.as_retriever(
        similarity_top_k=5,
        filters=[MetadataFilter(key="search_type", value="restaurant")]
    )
    bm25 = idx.as_retriever(similarity_top_k=5, vector_store_query_mode="hybrid", alpha=0.0)
    hret = idx.as_retriever(similarity_top_k=5, vector_store_query_mode="hybrid", alpha=0.75)
    hsnw = idx.as_retriever(similarity_top_k=5, vector_store_query_mode="hybrid", alpha=1.0)

    # Testing
    answers = {
        "regular": [],
        "regular_filtered": [],
        "bm25": [],
        "hybrid_retriever": [],
        "hsnw": [],
    }
    query = "testing, I would like to order a large pizza with mango, thai food, taco fiesta"
    for retriever in [
        (ret, "regular"),
        (ret2, "regular_filtered"),
        (bm25, "bm25"),
        (hret, "hybrid_retriever"),
        (hsnw, "hsnw")
    ]:
        ans = retriever[0].retrieve(query)
        for response in ans:
            answers[retriever[1]].append(
                (
                    response.metadata["restaurant_name"],
                    response.score if hasattr(response, 'score') else None,
                )
            )
    # Printing in ordered by score for all the retrievers
    print("Query: ", query)
    for retriever in answers:
        print(f"Retriever: {retriever}")
        for ans in sorted(answers[retriever], key=lambda x: x[1] if x[1] is not None else 0, reverse=True):
            print(ans)
        print("\n\n")

if __name__ == "__main__":
    main()