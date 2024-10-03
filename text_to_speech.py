from google.cloud import texttospeech
import os

def text_to_speech(text, json_key_file, output_filename):
    try:
        client = texttospeech.TextToSpeechClient.from_service_account_json(json_key_file)

        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-J"
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config
        )

        os.makedirs(os.path.dirname(output_filename), exist_ok=True)

        with open(output_filename, "wb") as out:
            out.write(response.audio_content)

        print(f"Text-to-speech output saved to: {output_filename}")
        return output_filename

    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        return None
