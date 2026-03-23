import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are ProAssist, an intelligent and motivating personal productivity assistant.
Your goal is to help the user organize tasks, set goals, apply productivity techniques, and stay motivated.
LANGUAGE RULE: Always respond in the same language the user writes in.
Use emojis in moderation. If the user shares a task, help them break it into concrete steps."""

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
        return jsonify({"error": "Mensaje vacío"}), 400

    conversation_history.append({"role": "user", "parts": [user_message]})

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=SYSTEM_PROMPT
    )
    chat = model.start_chat(history=conversation_history[:-1])
    response = chat.send_message(user_message)
    assistant_message = response.text

    conversation_history.append({"role": "model", "parts": [assistant_message]})
    return jsonify({"response": assistant_message})

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
