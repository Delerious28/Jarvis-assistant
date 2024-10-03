import os
import uuid

from text_to_speech import text_to_speech

FOLDER_PATH = "project"


def create_folder(folder_name):
    try:
        folder_path = os.path.join(FOLDER_PATH, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        response_text = f"Folder '{folder_name}' created successfully."
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_create_folder.mp3")
        text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
        return {"text": response_text, "filename": output_filename}
    except Exception as e:
        return {"text": f"Error creating folder '{folder_name}': {str(e)}"}

def create_file(file_name, content):
    try:
        file_path = os.path.join(FOLDER_PATH, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        response_text = f"File '{file_name}' created successfully with content."
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_create_file.mp3")
        text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
        return {"text": response_text, "filename": output_filename}
    except Exception as e:
        return {"text": f"Error creating file '{file_name}': {str(e)}"}

def list_files_and_folders():
    try:
        items = os.listdir(FOLDER_PATH)
        response_text = f"Files and folders: {', '.join(items)}"
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_list_files.mp3")
        text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
        return {"text": response_text, "filename": output_filename}
    except Exception as e:
        return {"text": f"Error listing files and folders: {str(e)}"}

def delete_file_or_folder(name):
    try:
        path = os.path.join(FOLDER_PATH, name)
        if os.path.isdir(path):
            os.rmdir(path)
            response_text = f"Folder '{name}' deleted successfully."
        elif os.path.isfile(path):
            os.remove(path)
            response_text = f"File '{name}' deleted successfully."
        else:
            response_text = f"No such file or folder: '{name}'"
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_delete.mp3")
        text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
        return {"text": response_text, "filename": output_filename}
    except Exception as e:
        return {"text": f"Error deleting '{name}': {str(e)}"}

def read_file_content(file_name):
    try:
        file_path = os.path.join(FOLDER_PATH, file_name)
        with open(file_path, "r") as file:
            content = file.read()
        response_text = f"Content of '{file_name}': {content}"
        output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_read_file.mp3")
        text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
        return {"text": response_text, "filename": output_filename}
    except Exception as e:
        return {"text": f"Error reading file '{file_name}': {str(e)}"}
    