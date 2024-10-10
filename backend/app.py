from flask import Flask
from flask_cors import CORS

from api.routes import api_bp
from backend.config import Config

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
