from flask import Flask
from flask_cors import CORS

# 追加インポート
from api.routes import api_bp

app = Flask(__name__)
CORS(app)

# OpenAIのAPIキーを設定
app.config["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Google Cloudのクライアントの初期化はroutes.py内で行います

# Blueprintをアプリに登録
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
