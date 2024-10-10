from google.cloud import speech, texttospeech
import openai


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
