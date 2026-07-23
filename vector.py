from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from reddit_bot import make_dataframe
import os
import pandas as pd
import uuid

DB_DIR = "./chroma_db"

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

def make_retriever(subreddit_name):
    print(f"Processing r/{subreddit_name} for make_retriever")

    collection_name = f"reddit_{subreddit_name.lower()}"  
    persist_path = os.path.join(DB_DIR, subreddit_name.lower())

    if os.path.exists(persist_path):
        print(f"Loading existing Chroma DB for r/{subreddit_name}")
        vector_store = Chroma(
            collection_name=collection_name,       
            embedding_function=embeddings,
            persist_directory=persist_path         
        )
        return vector_store.as_retriever(search_kwargs={"k": 5})
    
    df = make_dataframe(subreddit_name)

    documents = []                      
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row["title"] + " " + row["selftext"],
            metadata={
                "score": row["score"],
                "num_comments": row["num_comments"],
                "url": row["url"],
                "listing_type": row["listing_type"],
                "created_utc": row["created_utc"]
            }
        )

        documents.append(document)
        ids.append(str(uuid.uuid4()))

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_path
    )

    vector_store.add_documents(documents=documents, ids=ids)

    return vector_store.as_retriever(search_kwargs={"k": 5})