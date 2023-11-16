from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import os
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/process": {"origins": "http://127.0.0.1:5500"}})

# Replace 'your-openai-api-key' with your actual OpenAI API key
# It's better to use an environment variable for production
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.json
        print(data)
        text_response = client.chat.completions.create(
            messages=[{"role": "user", "content": data['text']}],
            model="gpt-4"
        ).choices[0].message.content

        # Now, convert the text response to speech
        speech_file_path = Path(__file__).parent / "speech.mp3"
        print("speech_file_path:", speech_file_path)
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text_response
        )
        speech_response.stream_to_file(str(speech_file_path))

        # You may want to send back the URL of the speech file or the file itself
        return jsonify({'reply': text_response, 'audio_url': '/speech.mp3'})
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': str(e)})
    

if __name__ == "__main__":
    app.run(debug=True)