import os
import uuid
import requests

from text_to_speech import text_to_speech


def search_images(query):
    try:
        api_key = '#google_api_key#'
        cx = '#Google Custom Search Engine ID#'
        endpoint = "https://www.googleapis.com/customsearch/v1"
        params = {"q": query, "cx": cx, "key": api_key, "searchType": "image"}

        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        if response.status_code == 200:
            results = response.json().get("items", [])
            if results:
                image_url = results[0]['link']
                response_text = f"Here is an image of {query}."
                directory = "speech_files"
                os.makedirs(directory, exist_ok=True)
                output_filename = os.path.join(directory, f"image_search_response_{uuid.uuid4().hex}.mp3")
                text_to_speech(response_text, 'voice-426815-41d982117f81.json', output_filename)
                return {"text": response_text, "filename": output_filename, "image_url": image_url}
            else:
                return {"text": "No image search results found."}
        else:
            return {"text": f"Image search failed with status code: {response.status_code}"}

    except requests.exceptions.HTTPError as http_err:
        return {"text": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"text": f"Error occurred during image search: {err}"}
