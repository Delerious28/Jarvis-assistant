import os
import uuid

from text_to_speech import text_to_speech


FOLDER_PATH = "project"

def store_user_data(filename, data):
    try:
        file_path = os.path.join(FOLDER_PATH, filename)
        with open(file_path, "a") as file:  
            file.write(data + "\n")
        response_text = f"Data stored in '{filename}'."
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_store_data.mp3")
        text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
        return {"text": response_text, "filename": output_filename}
    except Exception as e:
        return {"text": f"Error storing data in '{filename}': {str(e)}"}

def read_user_data(filename):
    try:
        file_path = os.path.join(FOLDER_PATH, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = file.readlines()
                profile_data = {}
                for line in data:
                    if line.startswith("Name:"):
                        profile_data["name"] = line.replace("Name:", "").strip()
                    elif line.startswith("Age:"):
                        profile_data["age"] = line.replace("Age:", "").strip()
                    elif line.startswith("Sex:"):
                        profile_data["sex"] = line.replace("Sex:", "").strip()
                return profile_data
        else:
            return None
    except Exception as e:
        return {"error": str(e)}