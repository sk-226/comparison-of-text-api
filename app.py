import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import torch

app = Flask(__name__)
CORS(app)

# SentenceTransformerモデルのロード（グローバルに一度だけロード）
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 環境変数からAPIキーを取得
# API_KEY = os.getenv('API_KEY')

def word_embedding_similarity(correct, proposed):
    correct_emb = model.encode(correct, convert_to_tensor=True)
    proposed_emb = model.encode(proposed, convert_to_tensor=True)

    cosine_sim = torch.nn.functional.cosine_similarity(correct_emb, proposed_emb, dim=0)
    return cosine_sim.item()

@app.route('/similarity', methods=['POST'])
def similarity():

    data = request.get_json()
    sentence_correct = data.get('sentence_correct')
    sentence_proposed = data.get('sentence_proposed')

    if not sentence_correct or not sentence_proposed:
        return jsonify({'error': 'Both sentence_correct and sentence_proposed are required.'}), 400

    # 類似度の計算
    similarity_score = word_embedding_similarity(sentence_correct, sentence_proposed)

    return jsonify({'similarity_score': similarity_score})

# Flaskの開発用サーバーは不要（Gunicornを使用）
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
