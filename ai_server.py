from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI-powered teacher designed to assist students in their learning journey. Your role is to provide professional, easy-to-understand, and concise answers to student questions. Make sure your explanations are clear, brief, and adapted to the student's level of understanding. When appropriate, include helpful examples or analogies to make the concepts easier to grasp. Always maintain a professional and friendly tone while encouraging curiosity and further learning."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("user_input", "")
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        response = chatbot_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
