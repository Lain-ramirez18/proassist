import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are ProAssist, an intelligent and motivating personal productivity assistant.
Your goal is to help the user:
- Organize tasks and daily priorities
- Create to-do lists and track progress
- Generate ideas and solutions to everyday problems
- Give productivity and wellness tips
- Summarize information and help make decisions

LANGUAGE RULE: Detect the language the user writes in and always respond in that same language.
If they write in Spanish, respond in Spanish. If they write in English, respond in English.
Use emojis in moderation to make responses friendlier.
If the user shares a task, help them break it down into concrete steps."""
)

chat_session = model.start_chat(history=[])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Mensaje vacío"}), 400
    response = chat_session.send_message(user_message)
    return jsonify({"response": response.text})

@app.route("/reset", methods=["POST"])
def reset():
    global chat_session
    chat_session = model.start_chat(history=[])
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
