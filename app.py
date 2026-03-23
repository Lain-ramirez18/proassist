import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = "You are ProAssist, an intelligent and motivating personal productivity assistant. Help the user organize tasks, set goals, apply productivity techniques, and stay motivated. LANGUAGE RULE: Always respond in the same language the user writes in. Use emojis in moderation."

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "empty"}), 400

    conversation_history.append({"role": "user", "parts": [{"text": user_message}]})

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": conversation_history
    }

    response = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        json=payload
    )
    result = response.json()

    if "candidates" not in result:
        return jsonify({"response": "Error: " + str(result)}), 500

    assistant_message = result["candidates"][0]["content"]["parts"][0]["text"]
    conversation_history.append({"role": "model", "parts": [{"text": assistant_message}]})

    return jsonify({"response": assistant_message})

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
