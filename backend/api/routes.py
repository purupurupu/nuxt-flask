from flask import Blueprint, jsonify, request
from .chat import chat_with_gpt
from .nuxt_info import get_nuxt_info

api_bp = Blueprint("api", __name__)


@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400
    response = chat_with_gpt(data["message"])
    return jsonify(response)


@api_bp.route("/nuxt-info", methods=["GET"])
def nuxt_info():
    info = get_nuxt_info()
    return jsonify(info)
