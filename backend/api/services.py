import io
import wave
from google.cloud import speech, texttospeech
import openai
import logging

from auth import clients

logger = logging.getLogger(__name__)


def speech_to_text(audio_content):
    speech_client = clients["speech_client"]

    logger.info(f"受信した音声データの長さ: {len(audio_content)} バイト")
    logger.debug(f"音声データの先頭20バイト: {audio_content[:20]}")

    # WEBM OPUSとして処理
    sample_rate = 48000  # WEBM OPUSのデフォルトサンプルレート
    channels = 1  # モノラルを仮定

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=sample_rate,
        audio_channel_count=channels,
        language_code="ja-JP",
    )

    logger.info(f"Speech-to-Text API設定: {config}")

    try:
        response = speech_client.recognize(config=config, audio=audio)
        logger.info(f"API応答全体: {response}")

        if not response.results:
            logger.warning("音声認識結果がありません。")
            return None

        return response.results[0].alternatives[0].transcript
    except Exception as e:
        logger.error(f"音声認識中にエラーが発生しました: {e}")
        return None


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
    # 認証済みの Text-to-Speech クライアントを使用
    tts_client = clients["tts_client"]
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    try:
        logger.info(f"Text-to-Speech リクエスト: テキスト='{text}', 言語='ja-JP'")
        tts_response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        logger.info("Text-to-Speech 変換が成功しました")
        return tts_response.audio_content
    except Exception as e:
        logger.error(f"Text-to-Speech 変換中にエラーが発生しました: {e}")
        return None
