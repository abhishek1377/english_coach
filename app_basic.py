from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/process": {"origins": "http://127.0.0.1:5500"}})


# Replace 'your-openai-api-key' with your actual OpenAI API key
# It's better to use an environment variable for production
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/process', methods=['POST'])
def process_text():
    try:
        print(request)
        data = request.json
        print(data)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": data['text']}],
            model="gpt-4"  # Change to "gpt-4" or appropriate model as needed
        )
        return jsonify({'reply': response.choices[0].message.content})
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)