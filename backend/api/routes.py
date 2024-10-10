from flask import Blueprint, request, jsonify, send_file
import openai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import io

from .controllers import (
    process_audio_controller,
    chat_controller,
    get_nuxt_info_controller,
)

api_bp = Blueprint("api", __name__)

# Google Cloudのクライアントを初期化
# TODO:認証情報がないと立ち上げでエラーが出るのでコメントアウト、認証情報が手に入り次第解除


@api_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/process_audio", methods=["POST"])
def process_audio():
    return process_audio_controller()


@api_bp.route("/nuxt-info", methods=["GET"])
def nuxt_info():
    return get_nuxt_info_controller()


# 他のモジュールから必要な関数をインポート
from .nuxt_info import get_nuxt_info
