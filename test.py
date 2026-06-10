from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import make_retriever

model = OllamaLLM(model="llama3")

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

print(result)