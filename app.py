from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# 🧩 Configure Gemini API
os.environ["GOOGLE_API_KEY"] = ""  # Add your API key here
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Model
model = genai.GenerativeModel("gemini-2.5-flash")


# Function to generate quiz
def generate_quiz(topic, difficulty, num_questions, question_type):
    prompt = f"""
    Generate a {num_questions}-question quiz on "{topic}".
    Difficulty level: {difficulty}.
    Question type: {question_type} (multiple choice, true/false, or short answer).

    Format clearly like this:
    Q1. [Question]
    A) ...
    B) ...
    C) ...
    D) ...
    Correct Answer: [A/B/C/D or text]
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response else "No response from model."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        topic = request.form.get('topic', '')
        difficulty = request.form.get('difficulty', 'Medium')
        num_questions = request.form.get('num_questions', '5')
        question_type = request.form.get('question_type', 'Multiple Choice')

        quiz_text = generate_quiz(topic, difficulty, num_questions, question_type)

        # Send the quiz to a separate page
        return render_template('quiz.html', quiz=quiz_text, topic=topic)
    except Exception as e:
        return render_template('index.html', error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
