from flask import Flask, render_template, request, jsonify
from google import genai
from config import API_KEY

app = Flask(__name__)

client = genai.Client(
    api_key=API_KEY
)

chat_history = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    message = request.json["message"]

    chat_history.append(
        {
            "role": "user",
            "parts": [
                {"text": message}
            ]
        }
    )


    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=chat_history
    )


    chat_history.append(
        {
            "role": "model",
            "parts": [
                {"text": response.text}
            ]
        }
    )


    return jsonify({
        "reply": response.text
    })

@app.route("/clear", methods=["POST"])
def clear():

    global chat_history

    chat_history = []

    return jsonify({
        "status": "cleared"
    })

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )
