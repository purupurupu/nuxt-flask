from flask import Blueprint, jsonify

from .controllers import (
    process_audio_controller,
    get_nuxt_info_controller,
)

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/process_audio", methods=["POST"])
def process_audio():
    return process_audio_controller()


# @api_bp.route("/process_audio_test", methods=["POST"])
# def process_audio_test():
#     return process_audio_test_controller()


@api_bp.route("/nuxt-info", methods=["GET"])
def nuxt_info():
    return get_nuxt_info_controller()


# 他のモジュールから必要な関数をインポート
from .nuxt_info import get_nuxt_info
