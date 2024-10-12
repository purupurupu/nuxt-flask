from google.cloud import speech, texttospeech
import openai
import pyttsx3
import os
from threading import Lock
from contextlib import contextmanager

# グローバル変数としてエンジンを作成し、ロックを使用して同期化
engine = pyttsx3.init()
engine_lock = Lock()


@contextmanager
def get_engine():
    global engine
    with engine_lock:
        if engine is None:
            engine = pyttsx3.init()
        try:
            yield engine
        finally:
            engine.endLoop()


def speech_to_text(audio_content):
    speech_client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="ja-JP",
    )

    response = speech_client.recognize(config=config, audio=audio)

    if not response.results:
        return None

    return response.results[0].alternatives[0].transcript


def normalize_text(text):
    prompt = f"次のテキストを正規化してください：{text}"
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.5,
    )

    return gpt_response.choices[0].text.strip()


def text_to_speech(text):
    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.WAV
    )

    tts_response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return tts_response.audio_content


# NOTE: フロントエンドテスト用。GoogleAPIの代わりにpyttsx3を使って音声を生成する
def text_to_speech_test(text):
    try:
        with get_engine() as current_engine:
            # 音声の設定（日本語の声が利用可能な場合）
            voices = current_engine.getProperty("voices")
            japanese_voice = next(
                (voice for voice in voices if "japanese" in voice.languages), None
            )
            if japanese_voice:
                current_engine.setProperty("voice", japanese_voice.id)

            # 一時ファイル名を生成
            temp_file = f"temp_{os.getpid()}_{os.urandom(4).hex()}.wav"

            # 音声をファイルに保存
            current_engine.save_to_file(text, temp_file)
            current_engine.runAndWait()

            # ファイルを読み込んでバイトデータとして返す
            with open(temp_file, "rb") as f:
                audio_data = f.read()

            # 一時ファイルを削除
            os.remove(temp_file)

            return audio_data

    except Exception as e:
        raise Exception(f"音声生成中にエラーが発生しました: {str(e)}")
