from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
from sentence_transformers import SentenceTransformer, util
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Intents with patterns
intents = [
    {
        "tag": "greeting",
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
        "responses": ["Hello! How can I help you with business ideas today?", "Hi there! Ready to explore some business concepts?", "Hey! What business topic interests you?"]
    },
    {
        "tag": "business_idea",
        "patterns": ["business idea", "startup idea", "new business", "entrepreneur"],
        "responses": ["I can help you generate business ideas! What industry interests you?", "Let's brainstorm some business concepts. What problem would you like to solve?", "Great! I have lots of business ideas. What's your area of interest?"]
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "goodbye", "see you later", "thanks"],
        "responses": ["Goodbye! Come back anytime for more business insights.", "Thanks for chatting! Have a great day.", "See you later! Keep building your business dreams."]
    }
]

# Precompute embeddings for patterns
pattern_embeddings = []
pattern_intents = []
for intent in intents:
    for pattern in intent["patterns"]:
        embedding = model.encode(pattern, convert_to_tensor=True)
        pattern_embeddings.append(embedding)
        pattern_intents.append(intent)

def get_bot_response(message):
    message_embedding = model.encode(message, convert_to_tensor=True)
    
    # Compute similarities
    similarities = util.pytorch_cos_sim(message_embedding, pattern_embeddings)[0]
    
    # Find best match
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]
    
    if best_score > 0.5:  # Threshold
        intent = pattern_intents[best_idx]
        return random.choice(intent["responses"])
    
    # Default response
    return "I'm here to help with business ideas and concepts! Try asking about business ideas, planning, or analysis."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = get_bot_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)