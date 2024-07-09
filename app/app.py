from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and tokenizer
model_path = "./trained_model"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

# Set the pad token ID
model.config.pad_token_id = tokenizer.eos_token_id

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    
    # Encode input with attention mask
    inputs = tokenizer(question, return_tensors='pt', padding=True, truncation=True)
    outputs = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=50, num_return_sequences=1)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
