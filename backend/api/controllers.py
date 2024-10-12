from flask import request, jsonify, send_file
import io
from .services import (
    speech_to_text,
    normalize_text,
    text_to_speech,
)
import logging

# from ..auth import clients

from .nuxt_info import get_nuxt_info

logger = logging.getLogger(__name__)


def process_audio_controller():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "音声ファイルが見つかりません"}), 400

    audio_content = audio_file.read()

    # 音声をテキストに変換
    text = speech_to_text(audio_content)
    print(text)
    logger.info(text)

    if not text:
        return jsonify({"error": "音声を認識できませんでした"}), 400

    # テキストを正規化
    # normalized_text = normalize_text(text)

    # テキストを音声に変換
    audio_output = text_to_speech(text)

    return send_file(
        io.BytesIO(audio_output),
        mimetype="audio/wav",
        as_attachment=False,
        download_name="output.wav",
    )


def get_nuxt_info_controller():
    info = get_nuxt_info()
    return jsonify(info)
