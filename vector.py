from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from reddit_bot import df
import os
import pandas as pd
import uuid
import shutil

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
if os.path.exists(db_location):
    shutil.rmtree(db_location)

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
    uid = str(uuid.uuid4())
    ids.append(uid)
    documents.append(document)
        
vector_store = Chroma(
    collection_name="reddit_posts",
    persist_directory=db_location,
    embedding_function=embeddings
)

vector_store.add_documents(documents=documents, ids=ids)
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)