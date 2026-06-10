from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import make_retriever
from flask import Flask, render_template, request, jsonify

model = OllamaLLM(model="llama3")

app = Flask(__name__)

retriever_cache = {}

template = """
You are an expert on answering questions about the Subreddit

Here is the context: {context}

Here is the question: {question}

Provide a detailed, insightful, and helpful answer based only on the subreddit posts.
"""

prompt = ChatPromptTemplate.from_template(template=template)
chain = prompt | model

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    subreddit = data.get("subreddit")

    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        if subreddit not in retriever_cache:
            retriever_cache[subreddit] = make_retriever(subreddit)
        retriever = retriever_cache[subreddit]
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 

    context = retriever.invoke(question)
    result = chain.invoke({"context": context, "question": question})
    print(result)

    return jsonify({"answer": result})

if __name__ == "__main__":
    app.run(port=8000, debug=True)

# model = OllamaLLM(model="llama3")

# template = """
# You are an expert on answering questions about the Subreddit

# Here is the context: {context}

# Here is the question: {question}

# Provide a detailed, insightful, and helpful answer based only on the subreddit posts.
# """

# prompt = ChatPromptTemplate.from_template(template=template)
# chain = prompt | model

# question = "How do I make Python more useful in everyday tasks?"
# subreddit = "Python"
# retriever = make_retriever(subreddit)
# context = retriever.invoke(question)
# result = chain.invoke({"context": context, "question": question})

# print(result)