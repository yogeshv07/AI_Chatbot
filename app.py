from flask import Flask, render_template, request
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
@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""
    question = ""
    selected_model = "Gemini 2.5 Flash"

    if request.method == "POST":

        question = request.form["question"]
        selected_model = request.form["model"]

        try:

            if selected_model == "gemini":

                response = gemini_model.generate_content(question)
                answer = response.text

                selected_model = "Gemini 2.5 Flash"

            else:

                response = openrouter_client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

                answer = response.choices[0].message.content

        except Exception as e:
            answer = str(e)

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        selected_model=selected_model
    )

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )