from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from .env file
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")

# Create Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        try:
            response = model.generate_content(question)
            answer = response.text

        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template(
        "index.html",
        answer=answer,
        question=question if request.method == "POST" else ""
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)