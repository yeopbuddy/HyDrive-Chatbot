
import os
import json
import pandas as pd
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# --- Configuration ---
# IMPORTANT: Replace with your actual Pinecone credentials
PINECONE_API_KEY = "YOUR_API_KEY"
PINECONE_ENVIRONMENT = "YOUR_ENVIRONMENT"
PINECONE_INDEX_NAME = "chatbot-index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

app = Flask(__name__) # Initialize Flask App

pc = None 
model = None


def load_data(filepath): # Load and Preprocess Data
    with open(filepath, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    return pd.DataFrame(data)


def setup_pinecone(df): # Create Pinecone Index and Upsert Data
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating new index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=model.get_sentence_embedding_dimension(),
            metric='cosine'
        )
    else:
        print(f"Index '{PINECONE_INDEX_NAME}' already exists. Skipping creation.")

    index = pc.Index(PINECONE_INDEX_NAME)
    
    print("Creating embeddings and upserting data to Pinecone. This may take a moment...")
    batch_size = 100
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        questions = batch['question'].tolist()
        embeddings = model.encode(questions)
        
        vectors_to_upsert = []
        for idx, row in batch.iterrows():
            vectors_to_upsert.append({
                "id": row['qa_id'],
                "values": embeddings[idx % batch_size].tolist(),
                "metadata": {"answer": row['answer']}
            })
        
        if vectors_to_upsert:
            index.upsert(vectors=vectors_to_upsert)
    print("Data upserted successfully.")

@app.route('/chat', methods=['POST']) # Flask API Endpoint for Chatbot
def chat():
    data = request.get_json()
    user_question = data.get('question')

    if not user_question:
        return jsonify({"error": "Question not provided"}), 400

    question_embedding = model.encode(user_question).tolist()

    index = pc.Index(PINECONE_INDEX_NAME)
    query_response = index.query(
        vector=question_embedding,
        top_k=1,
        include_metadata=True
    )

    if query_response['matches']:
        best_match = query_response['matches'][0]
        answer = best_match['metadata']['answer']
        return jsonify({"answer": answer})
    else:
        return jsonify({"answer": "Sorry, I don't have an answer to that question."})

if __name__ == '__main__':
    if PINECONE_API_KEY == "YOUR_API_KEY" or PINECONE_ENVIRONMENT == "YOUR_ENVIRONMENT":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: Please open chatbot/app.py and replace       !!!")
        print("!!!        \"YOUR_API_KEY\" and \"YOUR_ENVIRONMENT\" with your actual   !!!")
        print("!!!        Pinecone credentials.                                  !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        try:
            print("Initializing Pinecone...")
            pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
            
            print("Loading embedding model...")
            model = SentenceTransformer(EMBEDDING_MODEL)
            
            print("Loading data file...")
            df = load_data("YOUR_JSONL_DATA_PATH")

            setup_pinecone(df)
            
            print("\nSetup complete. Starting Flask server on http://0.0.0.0:5000")
            print("You can now send questions to http://localhost:5000/chat")
            print("Press Ctrl+C to stop the server.")
            
            app.run(host='0.0.0.0', port=5000)

        except Exception as e:
            print(f"An error occurred: {e}")
