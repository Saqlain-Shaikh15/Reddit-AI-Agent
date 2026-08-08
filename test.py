from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from vector import make_retriever

""" Use this script to test the connection to Reddit"""

model = ChatGroq(
    model="llama-3.3-70b-versatile", 
    api_key=os.getenv("groq_api"),
    temperature=0
)

template = """
You are an expert on answering questions about the Subreddit

Here is the context: {context}

Here is the question: {question}

Provide a detailed, insightful, and helpful answer based only on the subreddit posts.
"""

prompt = ChatPromptTemplate.from_template(template=template)
chain = prompt | model

question = "How do I make Python more useful in everyday tasks?"
subreddit = "pl"
retriever = make_retriever(subreddit)
context = retriever.invoke(question)
result = chain.invoke({"context": context, "question": question})

# print(result)