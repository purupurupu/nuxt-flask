from google.cloud import texttospeech, speech
import os
from dotenv import load_dotenv
import pathlib
import logging

logger = logging.getLogger(__name__)


def authenticate_clients():
    """
    Text-to-SpeechおよびSpeech-to-Text APIの認証を行い、クライアントを初期化する
    """
    # .env ファイルのパスを指定して環境変数を読み込む
    env_path = pathlib.Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    # 環境変数からサービスアカウントキーのパスを取得
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "環境変数 GOOGLE_APPLICATION_CREDENTIALS が設定されていません。"
        )

    # サービスアカウントキーのパスを環境変数に設定
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    try:
        # Text-to-Speech クライアントの初期化
        tts_client = texttospeech.TextToSpeechClient()
        logger.info("Text-to-Speech クライアントを初期化しました。")

        # Speech-to-Text クライアントの初期化
        speech_client = speech.SpeechClient()
        logger.info("Speech-to-Text クライアントを初期化しました。")

        return {"tts_client": tts_client, "speech_client": speech_client}

    except Exception as e:
        logger.error(f"クライアントの初期化中にエラーが発生しました: {e}")
        raise e


# クライアントをモジュールレベルで初期化
clients = authenticate_clients()

if __name__ == "__main__":
    try:
        clients = authenticate_clients()
        print("認証に成功しました。")
    except Exception as e:
        print(f"認証に失敗しました: {e}")
