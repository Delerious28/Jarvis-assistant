import os
import subprocess
import uuid
from googleapiclient.discovery import build
from text_to_speech import text_to_speech

def search_youtube_video(query, json_key_file):
    try:
        API_KEY = '#youtube_api_key#'
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=1,
            type='video'
        ).execute()

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                video_id = search_result['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                firefox_path = r'C:/Program Files/Mozilla Firefox/firefox.exe'  
                subprocess.Popen([firefox_path, '-new-tab', video_url])
                output_filename = os.path.join("speech_files", f"{uuid.uuid4().hex}_youtube.mp3")
                text_to_speech("Here you go.", json_key_file, output_filename)
                return {"text": "Here you go.", "filename": output_filename}

        return {"text": "No video found."}

    except Exception as e:
        return {"text": f"Error searching YouTube video: {str(e)}"}
