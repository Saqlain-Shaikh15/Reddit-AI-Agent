from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from vector import make_retriever
from reddit_bot import do_subreddit_exist
from flask import Flask, render_template, request, jsonify
import os

model = ChatGroq(
    model="llama-3.3-70b-versatile", 
    api_key=os.getenv("groq_api"),
    temperature=0
)

app = Flask(__name__)

retriever_cache = {}

template = """
You are an expert assistant that answers questions using information from Reddit posts.

You are given a collection of posts retrieved from a subreddit. These posts are your ONLY source of information.

Instructions:
- Answer the user's question directly.
- Synthesize information from multiple posts instead of describing each document.
- Do NOT list document IDs, metadata, scores, or comment counts.
- Do NOT say things like "the context says", "the posts mention", or "Document 1".
- Write naturally, as if you personally analyzed the subreddit discussions.
- If different posts disagree, mention the differing viewpoints.
- If the context does not contain enough information, say:
  "I couldn't find enough information in the retrieved subreddit posts to answer that."
- Do not make up information that is not supported by the context.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template=template)
chain = prompt | model

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check-subreddit", methods=["POST"])
def check_subreddit():
    data = request.get_json()
    subreddit = data["subreddit"]

    exists = do_subreddit_exist(subreddit)
    return jsonify({"exists": exists})

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
    # print(result)

    return jsonify({"answer": result.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)