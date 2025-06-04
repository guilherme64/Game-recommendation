from flask import Flask, request, render_template, jsonify
import requests
import json
from dotenv import load_dotenv
load_dotenv()  # Load from .env
import os



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    print("Received data:", data)
    games = list(data.values())  # Convert dictionary values to list
    print("Games array:", games)
    #return jsonify({"message": "Success", "received": games})
    return getAIResponse(games);


def getAIResponse(data):
    auth = "Bearer {}".format(os.getenv("API_KEY"))
    games = ', '.join(data)
    
    prmpt = "I played these games:{}, tell me one game that i could play based on them. Just give me the name of the game".format(games)
    print(prmpt)
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
          },
        data=json.dumps({
            "model": "deepseek/deepseek-prover-v2:free",
            "temperature": 0.9,
            "max_tokens": 100,
            "messages": [
            {
                "role":"system",
                "content":"you are a concise videogames recommendation system. Just return the name of the games"
            },
            {   
                "role": "user",
                "content": prmpt
            }
            ],
            
        })
    )
    response_data = response.json()
    message_content = message_content.replace('```python\n', '').replace('\n```', '')
    message_content = message_content.strip('"')
    return jsonify({"recommendation": message_content})

if __name__ == '__main__':
    app.run(debug=True)
