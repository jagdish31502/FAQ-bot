from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.llm_model import llm_model
from utils.embedding_model import embedding_model
from utils.helper_functions import *
from ddl.migrations import *
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

file_path = None

@app.route('/product_pdf', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            global file_path
            file = request.files['file']
            file_name = file.filename
            file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), file_name)
            file.save(file_path)
            if not file_name:
                raise ValueError("No file name provided")
            embeddings = embedding_model()
            insert_into_chromadb(file_path, embeddings)
            return jsonify(f"{file_name} uploaded successfully"), 200

        except Exception as e:
            return str(e), 500

@app.route('/FAQs', methods=['POST'])
def ask_question():
    if request.method == 'POST':
        try:
            if not file_path:
                return jsonify({"error": "No document uploaded"}), 400
            
            data = request.get_json()
            question = data['question']
            if not question:
                return jsonify({"error": "No question provided"}), 400
            embeddings = embedding_model()
            retriever = load_data(embeddings, file_path)
            if retriever is None:
                return jsonify({"error": "No document uploaded"}), 400
            llm = llm_model()
            response_json, error_message = prompt_template(llm, retriever, question)

            if response_json:
                response = response_json
                product_category = response.get('product_category', None)
                product_name = response.get('product_name', None)
                answer = response.get('answer', None)
                status_code = 200
            else:
                response = error_message
                status_code = 500

            message = insert_into_table(file_path, question, response, product_category, product_name, answer)
            return jsonify({"Question": question, "response": response, "message": message}), status_code
        
        except Exception as e:
            return str(e), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)