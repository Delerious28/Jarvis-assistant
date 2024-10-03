
import subprocess
import uuid
import psutil
import os
from text_to_speech import text_to_speech


def open_applications(command, json_key_file):
    try:
        words = command.split()
        applications = []

        for i in range(len(words)):
            if words[i] == "open" and i + 1 < len(words):
                application_name = words[i + 1]
                if application_name.lower() == "steam":
                    applications.append({"path": r'"C:\Program Files (x86)\Steam\steam.exe"', "text": "opening Steam."})

                elif application_name.lower() == "discord":
                    applications.append({"path": r'"C:\Users\beaum\AppData\Local\Discord\Update.exe" --processStart Discord.exe', "text": "opening Discord."})

                elif application_name.lower() == "plex":
                    applications.append({"path": r'"C:\Program Files\Plex\Plex\Plex.exe"', "text": "opening Plex."})

                elif application_name.lower() == "vs":
                    applications.append({"path": r'"C:\Users\beaum\AppData\Local\Programs\Microsoft VS Code\code.exe"', "text": "opening visual studio, happy coding sir."})

                elif application_name.lower() == "phpstorm":
                    applications.append({"path": r'"C:\Program Files\JetBrains\PhpStorm 2024.1.1\bin\phpstorm64.exe"', "text": "opening php storm, happy coding sir."})

                elif application_name.lower() == "destiny":
                    applications.append({"path": r'"E:\SteamLibrary\steamapps\common\Destiny 2\destiny2.exe"', "text": "starting destiny 2, enjoy killing gods sir."})

                elif application_name.lower() == "music":
                    url = "https://music.youtube.com/playlist?list=LM"
                    try:
                        subprocess.Popen([r'C:\Program Files\Mozilla Firefox\firefox.exe', url])
                        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_music.mp3")
                        text_to_speech("Youtube music is being opened.", json_key_file, output_filename)
                        return {"text": "Youtube music is being opened.", "filename": output_filename}
                    except Exception as e:
                        return {"text": f"Error opening Firefox with URL: {e}"}

                elif application_name.lower() == "nitrado":
                    url = "https://webinterface.nitrado.net/15435238/wi/gameserver/"
                    try:
                        subprocess.Popen([r'C:\Program Files\Mozilla Firefox\firefox.exe', url])
                        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_nitrado.mp3")
                        text_to_speech("Opening Nitrado web interface.", json_key_file, output_filename)
                        return {"text": "Opening Nitrado web interface.", "filename": output_filename}
                    except Exception as e:
                        return {"text": f"Error opening Firefox with URL: {e}"}

                elif application_name.lower() == "browser":
                    url = "http://127.0.0.1:5000/"
                    try:
                        subprocess.Popen([r'C:\Program Files\Mozilla Firefox\firefox.exe', url])
                        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_browser.mp3")
                        text_to_speech("Opening browser.", json_key_file, output_filename)
                        return {"text": "Opening browser.", "filename": output_filename}
                    except Exception as e:
                        return {"text": f"Error opening Firefox with URL: {e}"}

                elif application_name.lower() == "tweakers":
                    url = "https://tweakers.net"
                    try:
                        subprocess.Popen([r'C:\Program Files\Mozilla Firefox\firefox.exe', url])
                        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_tweakers.mp3")
                        text_to_speech("Opening tweakers.", json_key_file, output_filename)
                        return {"text": "Opening tweakers.", "filename": output_filename}
                    except Exception as e:
                        return {"text": f"Error opening Firefox with URL: {e}"}

        if applications:
            for app_info in applications:
                try:
                    subprocess.Popen(app_info["path"])
                    output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_open_app.mp3")
                    text_to_speech(app_info["text"], json_key_file, output_filename)
                    return {"text": app_info["text"], "filename": output_filename}
                except Exception as e:
                    return {"text": f"Error opening {app_info['path']}: {e}"}
        else:
            return {"text": "No applications specified."}

    except Exception as e:
        return {"text": f"Error opening application: {e}"}

def close_applications(command, json_key_file):
    try:
        words = command.split()
        applications = []

        for i in range(len(words)):
            if words[i] == "close" and i + 1 < len(words):
                application_name = words[i + 1]
                if application_name.lower() == "steam":
                    applications.append({"name": "steam.exe", "text": "closing Steam ."})
                
                elif application_name.lower() == "discord":
                    applications.append({"name": "Discord.exe", "text": "closing Discord."})
                
                elif application_name.lower() == "plex":
                    applications.append({"name": "Plex.exe", "text": "closing Plex."})
                
                elif application_name.lower() == "destiny":
                    applications.append({"name": "destiny2.exe", "text": "closing destiny 2."})

                elif application_name.lower() == "phpstorm":
                    applications.append({"name": "phpstorm64.exe", "text": "closing php storm."})

                elif application_name.lower() == "vs":
                    applications.append({"name": "code.exe", "text": "closing visual studio."})

        if applications:
            for app_info in applications:
                try:
                    for proc in psutil.process_iter():
                        if proc.name().lower() == app_info["name"].lower():
                            proc.kill()
                            output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_close_app.mp3")
                            text_to_speech(app_info["text"], json_key_file, output_filename)
                            return {"text": app_info["text"], "filename": output_filename}
                    return {"text": f"{app_info['name']} is not running."}
                except Exception as e:
                    return {"text": f"Error closing {app_info['name']}: {e}"}
        else:
            return {"text": "No applications specified to close."}

    except Exception as e:
        return {"text": f"Error closing application: {e}"}
