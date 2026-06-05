from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# OpenRouter
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

MODEL_LABELS = {
    "gemini": "Gemini 2.5 Flash",
    "openai/gpt-4o-mini": "GPT",
    "deepseek/deepseek-chat": "DeepSeek Chat",
    "meta-llama/llama-3.3-70b-instruct": "Llama 3.3",
    "qwen/qwen3-32b": "Qwen 3",
    "x-ai/grok-3-mini": "Grok",
}


def get_ai_answer(question, selected_model):
    if selected_model == "gemini":
        response = gemini_model.generate_content(question)
        return response.text

    response = openrouter_client.chat.completions.create(
        model=selected_model,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


def now_label():
    return datetime.now().strftime("%I:%M %p").lstrip("0")


@app.route("/", methods=["GET", "POST"])
def home():

    selected_model = session.get("selected_model", "gemini")
    messages = session.get("messages", [])

    if request.method == "POST":

        question = request.form.get("question", "").strip()
        selected_model = request.form.get("model", "gemini")
        session["selected_model"] = selected_model

        if question:
            messages.append({
                "role": "user",
                "content": question,
                "time": now_label()
            })

            try:
                answer = get_ai_answer(question, selected_model)
            except Exception as e:
                answer = str(e)

            messages.append({
                "role": "ai",
                "content": answer,
                "model": MODEL_LABELS.get(selected_model, selected_model),
                "time": now_label()
            })

            session["messages"] = messages

    return render_template(
        "index.html",
        messages=messages,
        model_labels=MODEL_LABELS,
        selected_model=selected_model
    )


@app.route("/new-chat", methods=["POST"])
def new_chat():
    session["messages"] = []
    return redirect(url_for("home"))

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
