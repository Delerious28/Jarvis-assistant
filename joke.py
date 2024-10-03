import os
import uuid
import requests

from text_to_speech import text_to_speech


def get_joke(json_key_file):
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)
    joke = response.json()
    
    if 'setup' not in joke or 'punchline' not in joke:
        response_text = "Error fetching joke."
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_joke_error.mp3")
        text_to_speech(response_text, json_key_file, output_filename)
        return {"text": response_text, "filename": output_filename}
    
    response_text = f"Here's a joke for you: {joke['setup']} {joke['punchline']}"
    output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_joke.mp3")
    text_to_speech(response_text, json_key_file, output_filename)
    
    return {"text": response_text, "filename": output_filename}
