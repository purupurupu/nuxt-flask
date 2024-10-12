from flask import request, jsonify, send_file
import io
from .services import (
    speech_to_text,
    normalize_text,
    text_to_speech,
    text_to_speech_test,
)
import speech_recognition as sr
from pydub import AudioSegment

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


# NOTE: テスト用。フロントからはformDataで送信する
# フロントまで3秒ぐらいで返ってくるので結構早いぞ？
def process_audio_test_controller():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "音声ファイルが見つかりません"}), 400

    recognizer = sr.Recognizer()

    try:
        # 一時的に音声ファイルを保存
        audio_bytes = audio_file.read()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # PCM WAVに変換
        wav_io = io.BytesIO()
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # 音声認識
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)

        # 音声をテキストに変換
        text = recognizer.recognize_google(audio_data, language="ja-JP")
        print(f"認識したテキスト: {text}")

        # NOTE: textを返却するテスト用のデバッグコード
        # return jsonify({"text": text}), 200

        # FIXME: ここでGPTを使って正規化をするフローがある
        # normalized_text = normalize_text(text)

        # FIXME: pyttsx3を使ってテキストを音声に変換。GoogleAPIの代わりになる
        audio_output = text_to_speech_test(text)

        return send_file(
            io.BytesIO(audio_output),
            mimetype="audio/wav",
            as_attachment=False,
            download_name="output.wav",
        )

    except sr.UnknownValueError:
        return jsonify({"error": "音声を認識できませんでした"}), 400
    except sr.RequestError as e:
        print(f"エラー詳細: {str(e)}")
        return (
            jsonify({"error": f"音声認識サービスにアクセスできませんでした"}),
            500,
        )
    except Exception as e:
        print(f"エラー詳細: {str(e)}")
        return jsonify({"error": f"予期せぬエラーが発生しました"}), 500


def get_nuxt_info_controller():
    info = get_nuxt_info()
    return jsonify(info)
