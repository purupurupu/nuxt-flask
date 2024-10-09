from flask import Flask
from api.routes import api_bp
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Blueprintの登録
    app.register_blueprint(api_bp, url_prefix="/api")

    # ヘルスチェック用ルート
    @app.route("/")
    def hello():
        return {"message": "Welcome to the API"}

    # エラーハンドリング
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
