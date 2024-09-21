# ベースイメージとしてPython 3.9のスリム版を使用
FROM python:3.9-slim

# 作業ディレクトリを /app に設定
WORKDIR /app

# システムパッケージの更新と必要なパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコンテナにコピー
COPY app.py .

# ポート8080を開放
EXPOSE 8080

# Gunicornを使用してアプリケーションを起動
CMD gunicorn --bind 0.0.0.0:$PORT app:app --log-level info --workers 4
