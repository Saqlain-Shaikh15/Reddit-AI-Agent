from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from flask import Flask, render_template, request, jsonify

model = OllamaLLM(model="llama3")

app = Flask(__name__)

template = """
You are an expert on answering questions about the Subreddit

Here is the subreddit: {context}

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
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    context = retriever.invoke(question)
    result = chain.invoke({"context": context, "question": question})

    return jsonify({"answer": result})


if __name__ == "__main__":
    app.run(debug=True)
