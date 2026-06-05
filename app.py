from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AQ.Ab8RN6KaONFd_vrP07hQd0WxGXOawZfTcY8oY3sMC-GbfrL3pw")

model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":
        question = request.form["question"]

        response = model.generate_content(question)

        answer = response.text

    return render_template(
        "index.html",
        answer=answer
    )

if __name__ == "__main__":
    app.run(debug=True)