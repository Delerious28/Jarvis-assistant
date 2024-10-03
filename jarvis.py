import os
import shutil
import threading
import requests
import subprocess
import psutil
import uuid
import pygame
import speech_recognition as sr
from google.cloud import texttospeech
from flask import Flask, request, jsonify, render_template
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os.path
import socket
import time

pygame.init()
pygame.mixer.init()

from defs.search_youtube_video import search_youtube_video
from defs.files import create_file, create_folder, delete_file_or_folder, list_files_and_folders, read_file_content
from defs.open_close import open_applications, close_applications
from text_to_speech import text_to_speech
from defs.openai_interaction import ask_openai  
from defs.backup import backup
from defs.news import get_news, process_news_request
from defs.wol import wake_on_lan
from defs.img_search import search_images
from defs.joke import get_joke
from defs.shutdownrestart import shutdown_system, restart_system
from defs.data import store_user_data, read_user_data

app = Flask(__name__, static_url_path='/static')

listening = False

profile_creation_state = {
    "in_progress": False,
    "name": None,
    "age": None,
    "sex": None
}


def play_audio(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"Error playing audio: {e}")


def recognize_and_execute(user_input, json_key_file):
    global listening, profile_creation_state

    try:
        text = user_input.strip().lower()
        print("Recognized user input:", text)

        if listening:
            if "stop" in text:
                pygame.mixer.music.stop()
                listening = False
                return {"text": "Operation stopped."}

            if profile_creation_state["in_progress"]:
                if profile_creation_state["name"] is None:
                    profile_creation_state["name"] = text.strip().capitalize()
                    response_text = "Got it. How old are you?"
                    output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_ask_age.mp3")
                    text_to_speech(response_text, json_key_file, output_filename)
                    return {"text": response_text, "filename": output_filename}
                
                elif profile_creation_state["age"] is None:
                    try:
                        profile_creation_state["age"] = int(text.strip())
                        response_text = "Thank you. Are you male or female?"
                        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_ask_sex.mp3")
                        text_to_speech(response_text, json_key_file, output_filename)
                        return {"text": response_text, "filename": output_filename}
                    except ValueError:
                        response_text = "Please provide a valid age."
                        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_invalid_age.mp3")
                        text_to_speech(response_text, json_key_file, output_filename)
                        return {"text": response_text, "filename": output_filename}
                
                elif profile_creation_state["sex"] is None:
                    profile_creation_state["sex"] = text.strip().capitalize()
                    filename = f"{profile_creation_state['name']}data.txt"
                    data = f"Name: {profile_creation_state['name']}\nAge: {profile_creation_state['age']}\nSex: {profile_creation_state['sex']}"
                    response = store_user_data(filename, data)
                    profile_creation_state = {"in_progress": False, "name": None, "age": None, "sex": None}
                    return response

            elif "open" in text:
                response = open_applications(text, json_key_file)
                return response

            elif "close" in text:
                response = close_applications(text, json_key_file)
                return response

            elif any(keyword in text for keyword in ["show me an image of", "show me a image of", "show me an image for", "show me a image for"]):
                query = text.replace("show me an image of", "").replace("show me a image of", "").replace("show me an image for", "").replace("show me a image for", "").strip()
                response = search_images(query)
                return response

            elif "create folder" in text:
                folder_name = text.replace("create folder", "").strip()
                response = create_folder(folder_name)
                return response

            elif "create file" in text:
                parts = text.replace("create file", "").strip().split(" with content ")
                file_name = parts[0].strip()
                content = parts[1].strip() if len(parts) > 1 else ""
                response = create_file(file_name, content)
                return response

            elif "list files" in text or "list folders" in text:
                response = list_files_and_folders()
                return response

            elif "delete" in text:
                name = text.replace("delete", "").strip()
                response = delete_file_or_folder(name)
                return response

            elif "read file" in text:
                file_name = text.replace("read file", "").strip()
                response = read_file_content(file_name)
                return response

            elif "shutdown" in text:
                text_to_speech("Shutting down the system, See ya", json_key_file, 'speech_files/shutdown_message.mp3')
                return shutdown_system()

            elif "restart" in text or "reboot" in text:
                text_to_speech("Restarting the system, See ya", json_key_file, 'speech_files/restart_message.mp3')
                return restart_system()

            elif "look on youtube for" in text or "play" in text:
                query = text.replace("look on youtube for", "").strip()
                response = search_youtube_video(query, json_key_file)
                return response

            elif "that's all" in text or "i'm done" in text or "bye" in text:
                listening = False
                audio_file = r"start.wav"
                play_audio(audio_file)

            elif "create new profile" in text or "new person" in text:
                profile_creation_state["in_progress"] = True
                response_text = "Okay, let's create a new profile. What is your name?"
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_ask_name.mp3")
                text_to_speech(response_text, json_key_file, output_filename)
                return {"text": response_text, "filename": output_filename}

            elif "what's my name" in text or "what is my name" in text or "say my name" in text:
                profile_data = read_user_data("Beaudata.txt") 
                if profile_data and "name" in profile_data:
                    response_text = f"Your name is {profile_data['name']}."
                else:
                    response_text = "I don't have your name stored."
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_name_response.mp3")
                text_to_speech(response_text, json_key_file, output_filename)
                return {"text": response_text, "filename": output_filename}

            elif "what is my age" in text or "how old am i" in text or "what's my age" in text:
                profile_data = read_user_data("Beaudata.txt")  
                if profile_data and "age" in profile_data:
                    response_text = f"You are {profile_data['age']} years old."
                else:
                    response_text = "I don't have your age stored."
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_age_response.mp3")
                text_to_speech(response_text, json_key_file, output_filename)
                return {"text": response_text, "filename": output_filename}

            elif "what is my sex" in text or "what's my sex" in text or "what gender am i" in text or "what's my gender" in text or "what is my gender" in text:
                profile_data = read_user_data("Beaudata.txt")  
                if profile_data and "sex" in profile_data:
                    response_text = f"Your sex is {profile_data['sex']}."
                else:
                    response_text = "I don't have your sex stored."
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_sex_response.mp3")
                text_to_speech(response_text, json_key_file, output_filename)
                return {"text": response_text, "filename": output_filename}
    
            elif "backup" in text:
                source_folder = r'C:\Users\beaum\Desktop\Jarvis Web'  
                destination_folder = r'C:\Users\beaum\Desktop\jarvis-backup'  
                response = backup(source_folder, destination_folder)
                response_text = "backing up your code now"
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_backup_complete.mp3")
                text_to_speech(response_text, json_key_file, output_filename)
                return {"text": response_text, "filename": output_filename}
            
            elif "turn on pc" in text:
                mac_address = "2C:F0:5D:E8:FD:18"
                wake_on_lan(mac_address)
                return {"text": "PC is turning on."}

            elif "tell me a joke" in text:
                response = get_joke(json_key_file)  
                return response

            else:
                conversation_history = []  
                response_text = ask_openai(text, conversation_history)
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_openai_response.mp3")
                text_to_speech(response_text, json_key_file, output_filename)
                return {"text": response_text, "filename": output_filename}

        else:
            if "jarvis" in text or "dave" in text:
                listening = True
                audio_file = r"start.wav"
                play_audio(audio_file)

            else:
                return {"text": ""}

    except Exception as e:
        return {"text": f"Error: {str(e)}"}


@app.route('/')
def index():
    return render_template('index.php')

@app.route('/command', methods=['POST'])
def handle_command():
    try:
        data = request.get_json()
        command = data.get('command', '').lower()

        response = recognize_and_execute(command, 'voice-426815-41d982117f81.json')

        if "filename" in response:
            play_audio(response["filename"]) 

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": {"text": f"Error handling command: {e}"}})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
