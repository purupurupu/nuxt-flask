from flask import request, jsonify, send_file
import openai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import io
from .services import speech_to_text, normalize_text, text_to_speech

# Google Cloudのクライアントを初期化
# TODO: 認証情報がないと立ち上げでエラーが出るのでコメントアウト、認証情報が手に入り次第解除
# speech_client = speech.SpeechClient()
# tts_client = texttospeech.TextToSpeechClient()

from .nuxt_info import get_nuxt_info


def process_audio_controller():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "音声ファイルが見つかりません"}), 400

    audio_content = audio_file.read()

    # 音声をテキストに変換
    text = speech_to_text(audio_content)
    if not text:
        return jsonify({"error": "音声を認識できませんでした"}), 400

    # テキストを正規化
    normalized_text = normalize_text(text)

    # テキストを音声に変換
    audio_output = text_to_speech(normalized_text)

    return send_file(
        io.BytesIO(audio_output),
        mimetype="audio/wav",
        as_attachment=False,
        attachment_filename="output.wav",
    )


def get_nuxt_info_controller():
    info = get_nuxt_info()
    return jsonify(info)
