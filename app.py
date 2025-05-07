from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import random

app = Flask(__name__, template_folder=r"D:\MindfulAI\Project  mental-wellness-assistant\models\template")

# Initialize Gemini
genai.configure(api_key="AIzaSyCahzWmasVd9pkUGYKx4uOQIGSFlqUx5W4")  
model = genai.GenerativeModel("models/gemini-2.0-pro-exp")

starting_questions = [
    "How are you feeling today?",
    "Can you describe your mood right now?",
    "Have you noticed any changes in your emotional state today?"
]

chat_log = []
round_counter = 0
max_rounds = 10


@app.route("/", methods=["GET", "POST"])
def index():
    global chat_log, round_counter

    if not chat_log:
        question = random.choice(starting_questions)
        chat_log.append(("assistant", question))

    if request.method == "POST":
        user_input = request.form.get("message", "").strip()
        if not user_input:
            return redirect(url_for("index"))

        chat_log.append(("user", user_input))
        round_counter += 1

        # Build history
        qa_pairs = []
        for i in range(1, len(chat_log), 2):
            if chat_log[i - 1][0] == "assistant":
                q = chat_log[i - 1][1]
                a = chat_log[i][1]
                qa_pairs.append((q, a))

        history = "\n".join([f"User: {a}\nAssistant: {q}" for q, a in qa_pairs])

        prompt = f"""
You are a warm, empathetic mental wellness assistant.

Here is the conversation so far:
{history}

Now respond with:
1. Avoid complimenting or repeating the same phrasing.
2. A meaningful follow-up question about their feelings, stress, energy, or sleep. Make sure it's not a repetitive or overly similar question from earlier.

Only output these one responses, separated clearly.
"""

        result = model.generate_content(prompt).text.strip()
        lines = [line.strip() for line in result.split("\n") if line.strip()]
        empathic = ""
        next_question = ""

        for line in lines:
            if "?" in line:
                next_question = line
                break
            else:
                empathic += line + " "

        if not next_question:
            next_question = "Can you tell me more about how you're feeling?"

        if empathic:
            chat_log.append(("assistant", empathic.strip()))
        chat_log.append(("assistant", next_question))

        if round_counter >= max_rounds:
            return redirect(url_for("report"))

    return render_template("index.html", chat=chat_log)


@app.route("/report")
def report():
    global chat_log

    qa_pairs = []
    for i in range(1, len(chat_log), 2):
        if chat_log[i - 1][0] == "assistant":
            q = chat_log[i - 1][1]
            a = chat_log[i][1]
            qa_pairs.append((q, a))

    conversation = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_pairs])

    prompt = f"""
You are a licensed digital wellness assistant. Based on the following conversation, provide:

1. only Scores (1-10) for:
   - Emotional Wellbeing
   - Stress Level
   - Sleep Quality
   - Energy and Motivation

Conversation:
{conversation}
"""

    result = model.generate_content(prompt).text.strip()
    return render_template("index.html", chat=chat_log, report=result)


@app.route("/reset")
def reset():
    global chat_log, round_counter
    chat_log = []
    round_counter = 0
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
