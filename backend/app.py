from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai

# 追加インポート
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import io

app = Flask(__name__)
CORS(app)

# OpenAIのAPIキーを設定
openai.api_key = "YOUR_OPENAI_API_KEY"

# Google Cloudのクライアントを初期化
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()


@app.route("/process_audio", methods=["POST"])
def process_audio():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "音声ファイルが見つかりません"}), 400

    audio_content = audio_file.read()

    # Speech-to-Textの設定
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="ja-JP",
    )

    # 音声をテキストに変換
    response = speech_client.recognize(config=config, audio=audio)

    if not response.results:
        return jsonify({"error": "音声を認識できませんでした"}), 400

    text = response.results[0].alternatives[0].transcript

    # GPTを使ってテキストを正規化
    prompt = f"次のオーダーを飲食店のメニューに基づいて正規化してください：{text}"
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.5,
    )

    normalized_text = gpt_response.choices[0].text.strip()

    # Text-to-Speechの設定
    synthesis_input = texttospeech.SynthesisInput(text=normalized_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.WAV
    )

    # 音声データを生成
    tts_response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return send_file(
        io.BytesIO(tts_response.audio_content),
        mimetype="audio/wav",
        as_attachment=False,
        attachment_filename="output.wav",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
